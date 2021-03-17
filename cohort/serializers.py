from rest_framework import serializers

from cohort.models import User


class BaseSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    # Extra feature (https://www.django-rest-framework.org/api-guide/serializers/#example)
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        super(BaseSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(BaseSerializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=254, required=False)
    is_active = serializers.BooleanField(read_only=True)

    displayname = serializers.CharField(max_length=50, required=False)
    firstname = serializers.CharField(max_length=30, required=False)
    lastname = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ("uuid", "created_at", "modified_at",
                  "username", "password", "email", "is_active",
                  "displayname", "firstname", "lastname",)

