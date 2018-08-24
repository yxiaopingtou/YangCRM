from django.test import TestCase

# Create your tests here.
import datetime

# b = datetime.datetime.now().strftime("%Y-%m-%d")
# print(type(b),b)

# a = {"name":1}
# for i in a.values():
#     print(i)

# list_display = ['name',
#                 'contact_type',
#                 'contact',
#                 'source',
#                 'referral_from',
#                 'consult_content',
#                 'status',
#                 'consultant',
#                 'date']
#
# print(type(list_display.index('contact')))

list_display = ['name',
                    'contact_type',
                    'contact',
                    'source',
                    'referral_from',
                    'consult_content',
                    'status',
                    'consultant',
                    'date']

for column in list_display:
    print(list_display.index(column))
