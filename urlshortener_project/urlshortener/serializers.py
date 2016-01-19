import string
from time import time
from itertools import chain
from random import seed, choice, sample

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ShortenedLink
from urlshortener_project.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class ShortenedLinkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    clicks = serializers.ReadOnlyField(source='hitNumber')


    class Meta:
        model = ShortenedLink
        fields = ['id', 'user', 'short', 'longURL', "created", "modified", "clicks"]

    def validate(self, attrs):
        instance = ShortenedLink(**attrs)
        instance.clean()
        return attrs


class CreateShortenedLinkSerializer(serializers.ModelSerializer):
    short = serializers.ReadOnlyField()

    class Meta:
        model = ShortenedLink
        fields = ['id','short','longURL']

    def generateCode(self):
        self.generatedCode = self.getCode()
        uniqueCode = self.unique_code()
        while (not uniqueCode):
            self.generatedCode = self.getCode()
            uniqueCode = self.unique_code()
        return self.generatedCode

    def unique_code(self):
        #Validate the uniqueness of self.short
        queryList = ShortenedLink.objects.filter(short=self.generatedCode)
        if queryList.exists():
            return False
        else:
            return True

    def getCode(self, length=5, digits=2, upper=0, lower=3):
        seed(time())

        lowercase = string.lowercase.translate(None, "o")
        uppercase = string.uppercase.translate(None, "O")
        letters = "{0:s}{1:s}".format(lowercase, uppercase)

        code = list(
            chain(
                (choice(uppercase) for _ in range(upper)),
                (choice(lowercase) for _ in range(lower)),
                (choice(string.digits) for _ in range(digits)),
                (choice(letters) for _ in range((length - digits - upper - lower)))
            )
        )

        return "".join(sample(code, len(code)))

