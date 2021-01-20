from tortoise import fields, models


class TimestampModelMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Demo(TimestampModelMixin, models.Model):
    """Demo Model """

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=20)

    class Meta:
        table = "demo"
