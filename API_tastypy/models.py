from django.db import models
from tastypie.resources import ModelResource
from AutamaProfiles.models import AutamaProfile
from accounts.models import User, Matches
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication
from tastypie.models import ApiKey
from django.urls import path
from django.conf.urls import url
from django.db import IntegrityError
from tastypie.exceptions import BadRequest
from accounts.models import Messages
from Nucleus.ham import Ham


class UnmatchedAutamaAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        matched_autama = Matches.objects.filter(userID=bundle.request.user)
        matched_autama = matched_autama.values('autamaID').distinct()
        unmatched_autama = AutamaProfile.objects.exclude(id__in=matched_autama)

        return unmatched_autama

class UnmatchedAutamaResource(ModelResource):
    class Meta:
        queryset = AutamaProfile.objects.all()
        resource_name = 'unmatchedautama'
        fields = ['id', 'creator', 'first', 'last', 'interest1', 'interest2', 'interest3', 'interest4', 'interest5',
                  'interest6', 'picture']

        authentication = BasicAuthentication()
        authorization = UnmatchedAutamaAuthorization()

    def hydrate(self, bundle):
        bundle.obj = None
        userID = User.objects.get(username=bundle.data.get('userID'))
        autamaID = AutamaProfile.objects.get(id=int(bundle.data.get('autamaID')))
        if not Matches.objects.filter(autamaID=autamaID).filter(userID=userID).exists():
            Matches(userID=userID, autamaID=autamaID).save()

        return bundle


class AccountAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id)


class AccountsResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'accounts'  # Change to 'login' end point
        fields = ['id', 'username']
        filtering = {
            'username': ['exact']
        }

        authorization = AccountAuthorization()
        authentication = BasicAuthentication()

    def dehydrate(self, bundle):
        username = bundle.request.headers.get('Username')
        user = User.objects.get(username=username)
        #apikey = ApiKey.objects.get(user=user)
        #bundle.data['apikey'] = apikey.key
        return bundle


class RegistrationResource(ModelResource):
    class Meta:
        resource_name = 'register'
        allowed_methods = ['post']
        object_class = User
        include_resource_uri = False

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            user = User.objects.create(username=bundle.data.get('username'))
            user.set_password(bundle.data.get('password'))
            user.save()
            #apikey = bundle.data.get('apikey')
            #user = User.objects.get(username=bundle.data.get('username'))
            #apikey = ApiKey.objects.create(key=apikey, user=user)
            #apikey.save()
            bundle.obj = user  # HAVE to update the bundle object to include its data in post response.
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle

class MessagingAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        autama_id = int(bundle.request.headers.get('AutamaID'))
        autama = AutamaProfile.objects.get(pk=autama_id)
        user = bundle.request.user
        return object_list.filter(userID=user).filter(autamaID=autama)


class MessagingResource(ModelResource):
    class Meta:
        queryset = Messages.objects.all()
        resource_name = 'messages'
        authorization = MessagingAuthorization()
        #authentication = ApiKeyAuthentication()
        authentication = BasicAuthentication()
        include_resource_uri = False
        fields = ['userID', 'autamaID', 'message', 'sender', 'timeStamp'] # Seems like atleast one of the fields in the post must be mentioned here to have them included in post response.
        always_return_data = True # Seems to need this get posted data returned in response.
        allowed_methods = ['post', 'get']

    def hydrate(self, bundle):
        user = User.objects.get(username=bundle.data.get("userID"))
        autama = AutamaProfile.objects.get(pk=int(bundle.data.get("autamaID")))
        message = bundle.data.get("message")
        sender = bundle.data.get("sender")
        message = Messages.objects.create(userID=user, autamaID=autama, sender=sender, message=message)
        #message.save() # somewhere in the hydrate cycle tastypie calls save for us
        bundle.obj = message

        return bundle

    def dehydrate(self, bundle):
        # Using HAM to get a response from Autama
        autama  = AutamaProfile.objects.get(pk=int(bundle.data.get("autamaID")))
        message = bundle.data.get("message")
        user    = User.objects.get(username=bundle.data.get("userID"))

        first_name = autama.first
        last_name  = autama.last
        trait1 = autama.interest1
        trait2 = autama.interest2
        trait3 = autama.interest3
        trait4 = autama.interest4
        trait5 = autama.interest5
        trait6 = autama.interest6
        personality     = [trait1, trait2, trait3, trait4, trait5, trait6]
        ham             = Ham(first_name, last_name, personality)
        autama_response = ham.converse(user_input=message)
        message         = Messages.objects.create(userID=user, autamaID=autama, sender="Autama", message=autama_response)
        message.save()

        autama    = str(message.autamaID.id)
        user      = message.userID.username
        sender    = message.sender
        timeStamp = str(message.timeStamp)
        message   = message.message

        bundle.data['autamaID']  = autama
        bundle.data['userID']    = user
        bundle.data['sender']    = sender
        bundle.data['timeStamp'] = timeStamp
        bundle.data['message']   = message

        return bundle

class MyMatchesAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        user = bundle.request.user
        return object_list.filter(userID=user)

class MyMatchesResource(ModelResource):
    class Meta:
        queryset = Matches.objects.all()
        resource_name = 'mymatches'
        authorization = MyMatchesAuthorization()
        #authentication = ApiKeyAuthentication()
        authentication = BasicAuthentication()

    def dehydrate(self, bundle):
        a_match  = Matches.objects.get(id=int(bundle.data.get("id")))
        userID   = str(a_match.userID.id)
        autamaID = str(a_match.autamaID.id)
        bundle.data['userID'] = userID
        bundle.data['autamaID'] = autamaID
        bundle.data['autamaFirstName'] = a_match.autamaID.first
        bundle.data['autamaLastName'] = a_match.autamaID.last

        return bundle
