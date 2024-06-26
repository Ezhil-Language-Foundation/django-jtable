from datetime import date, datetime
from urllib.request import Request

from django.db.models import Model, F
from django.http import JsonResponse, HttpRequest

class ModelViewBuilder:
    def __init__(self, ModelClass: Model, fields, editable, modifier={}, datefields=[]):
        self.pk_name = ModelClass.__name__ + "Id"
        self._ModelClass = ModelClass
        self._fields = fields
        self._editable = editable
        self._modifier = modifier
        self._datefields = datefields

    def update(self, request: Request):
        print("UPDATE ACTION")

        r = request.POST
        import pprint
        pprint.pprint(r)
        #breakpoint()
        target = self._ModelClass.objects.get(id=r.get(self.pk_name))

        kwargs = {name: r.get(fieldname) for name, fieldname in self._editable.items()}
        for name, modifier in self._modifier.items():
            kwargs[name] = modifier(kwargs[name])
        kwargs.pop('id')
        for _field,_value in kwargs.items():
            setattr(target,_field,_value)
        target.save()
        data = {"Result": "OK"}
        return JsonResponse(data)

        return None

    def read(self, request: Request):
        print("LIST ACTION")
        # '-' means descending
        print(request.POST)
        r = request.POST
        kwargs = {fieldname: F(name) for name, fieldname in self._fields.items()}
        print(kwargs)
        kwargs.update({"Id": F("id")})
        s = self._ModelClass.objects.values(**kwargs)

        # wrap .values() in list because it is not serializable into JSON
        records = list(s)

        for record in records:
            for datefield in self._datefields:
                if isinstance(record[datefield], (date, datetime)):
                    record[datefield] = record[datefield].isoformat()
            # update boolean fields for display
            for field in record.keys():
                if isinstance(record[field],bool):
                    record[field] = str(record[field])


        # sorting by field:
        sort_field = request.GET.get("jtSorting","")
        if sort_field:
            try:
                field, direction = sort_field.split(" ")
                reverse = direction.upper() == "DESC"
                records = sorted(records, key=lambda rec: rec[field], reverse=reverse)
            except Exception:
                pass

        # list(s) -> "Records"
        data = {"Result": "OK", "Records": records}

        print(records)
        return JsonResponse(
            data, safe=False
        )  # safe=False means types other than dict can be sent

    def create(self, request: Request):
        print("CREATE ACTION")
        r = request.POST
        kwargs = {name: r.get(fieldname) for name, fieldname in self._fields.items()}
        for name, modifier in self._modifier.items():
            kwargs[name] = modifier(kwargs[name])

        s = self._ModelClass.objects.create(**kwargs)

        record = kwargs
        record["id"] = s.id
        record["record_date"] = datetime.now().isoformat()[:19]

        data = {"Result": "OK", "Record": record}

        return JsonResponse(data)

    def delete(self, request: HttpRequest):
        print("DELETE ACTION")
        print(request)
        print(request.POST)

        r = request.POST
        target = self._ModelClass.objects.filter(id=r.get(self.pk_name))
        print(target)
        target.delete()

        data = {"Result": "OK"}
        return JsonResponse(data)
