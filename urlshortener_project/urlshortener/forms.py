import string
from time import time
from itertools import chain
from random import seed, choice, sample

from django.forms import ModelForm, URLInput, TextInput

from .models import ShortenedLink


class ShortendedLinkForm(ModelForm):
    class Meta:
        model = ShortenedLink
        fields = ['longURL']
        widgets = {
            'longURL': URLInput(attrs={'class': 'form-control', 'placeholder':'Paste your long URL here...', 'required':'true'}),
        }

    def generateCode(self):
        generatedCode = getCode()
        uniqueCode = self.unique_code(generatedCode)
        while (not uniqueCode):
            generatedCode = getCode()
            uniqueCode = self.unique_code(generatedCode)
        return generatedCode

    def unique_code(self, generatedCode):
        #Validate the uniqueness of self.short
        queryList = ShortenedLink.objects.filter(short=generatedCode)
        if queryList.exists():
            return False
        else:
            return True



class UpdateShortenedLinkForm(ModelForm):
    class Meta:
        model = ShortenedLink
        fields = ['short','longURL']
        widgets = {
            'short': TextInput(attrs={'class': 'form-control',
                                      'placeholder':'Shortened Link...',
                                      'required':'true',
                                      'nospace':'true',
                                      'specialCharacters':'true'
                                      }
                               ),
            'longURL': URLInput(attrs={'class': 'form-control',
                                       'placeholder':'Paste your long URL here...',
                                       'required':'true'
                                       }),
        }



def getCode(length=5, digits=2, upper=0, lower=3):
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
