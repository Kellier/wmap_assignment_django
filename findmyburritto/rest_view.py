from . import serializers

from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import permissions, authentication, status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon
from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes


class UsersList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserOtherSerializer

    def get_queryset(self):
        return get_user_model().objects.all().order_by("username")

    def get_serializer_context(self):
        return {"request": self.request}


class UserMe_R(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserMeSerializer

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)


class UserOther_R(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if "uid" in self.kwargs and self.kwargs["uid"]:
            users = get_user_model().objects.filter(id=self.kwargs["uid"])
        elif "email" in self.kwargs and self.kwargs["email"]:
            users = get_user_model().objects.filter(email=self.kwargs["email"])
        else:
            users = None
        if not users:
            self.other = None
            raise exceptions.NotFound
        self.other = users[0]
        return self.other

    def get_serializer_class(self):
        if self.request.user == self.other:
            return serializers.UserMeSerializer
        else:
            return serializers.UserOtherSerializer


class UpdatePosition(generics.UpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserMeSerializer

    # @method_decorator(csrf_exempt)
    # def dispatch(self, *args, **kwargs):
    #     return super(UpdatePosition, self).dispatch(*args, **kwargs)

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)

    def perform_update(self, serializer, **kwargs):
        try:
            lat1 = float(self.request.data.get("lat", False))
            lon1 = float(self.request.data.get("lon", False))
            # lat2 = float(self.request.query_params.get("lat", False))
            # lon2 = float(self.request.query_params.get("lon", False))
            if lat1 and lon1:
                point = Point(lon1, lat1)
            # elif lat2 and lon2:
            #     point = Point(lon2, lat2)
            else:
                point = None

            if point:
                # serializer.instance.last_location = point
                serializer.save(last_location = point)
            return serializer
        except:
            pass


@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
# @csrf_exempt
def token_login(request):
    if (not request.GET["username"]) or (not request.GET["password"]):
        return Response({"detail": "Missing username and/or password"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=request.GET["username"], password=request.GET["password"])
    if user:
        if user.is_active:
            login(request, user)
            try:
                my_token = Token.objects.get(user=user)
                return Response({"token": "{}".format(my_token.key)}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Could not get token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Inactive account"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Invalid User Id of Password"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", ])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def get_burritos(request):
    #
    # bounding box qry (50.745,7.17,50.75,7.18)
    import overpy
    api = overpy.Overpass()

    # area_name = request.query_params.get("areaname", "")
    cuisine = request.query_params.get("cuisine", "")
    bbox = request.query_params.get("bbox", "")

    query = """
    [out:json][timeout:25]; 
    (
        node({1})["cuisine"="{0}"]; 
        way({1})["cuisine"="{0}"]; 
        rel({1})["cuisine"="{0}"]; 
    ); 
    out center body qt; 
    """.format(cuisine, bbox)

    try:
        result = api.query(query)

        result_geojson = {"type": "FeatureCollection", "features": []}
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [None, None]
            },
            "properties": {
            }
        }

        for node in result.nodes:
            this_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [None, None]
                },
                "properties": {
                }
            }

            this_feature["geometry"]["coordinates"][0] = float(node.lon)
            this_feature["geometry"]["coordinates"][1] = float(node.lat)

            for tag in node.tags:
                this_feature["properties"][tag] = node.tags[tag]

            result_geojson["features"].append(this_feature)

        for way in result.ways:
            this_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [None, None]
                },
                "properties": {
                }
            }

            this_feature["geometry"]["coordinates"][0] = float(way.center_lon)
            this_feature["geometry"]["coordinates"][1] = float(way.center_lat)

            for tag in way.tags:
                this_feature["properties"][tag] = way.tags[tag]

            result_geojson["features"].append(this_feature)

        return Response(result_geojson, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)

