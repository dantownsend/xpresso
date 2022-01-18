import json
import sys
import typing

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

import xpresso._param_dependants as param_dependants
from xpresso._extractors.body.discriminated import (
    ContentTypeDiscriminatedExtractorMarker,
)
from xpresso._extractors.body.field import (
    FieldExtractorMarker,
    RepeatedFieldExtractorMarker,
)
from xpresso._extractors.body.file import FileBodyExtractorMarker
from xpresso._extractors.body.form import (
    FormDataBodyExtractorMarker,
    MultipartBodyExtractorMarker,
)
from xpresso._extractors.body.form_field import FormFieldBodyExtractorMarker
from xpresso._extractors.body.json import Decoder, JsonBodyExtractorMarker
from xpresso._extractors.params.cookie import CookieParameterExtractorMarker
from xpresso._extractors.params.header import HeaderParameterExtractorMarker
from xpresso._extractors.params.path import PathParameterExtractorMarker
from xpresso._extractors.params.query import QueryParameterExtractorMarker
from xpresso._openapi_providers.body.discriminated import (
    OpenAPIContentTypeDiscriminatedMarker,
)
from xpresso._openapi_providers.body.field import (
    OpenAPIFieldMarker,
    OpenAPIRepeatedFieldMarker,
)
from xpresso._openapi_providers.body.file import OpenAPIFileMarker
from xpresso._openapi_providers.body.form import OpenAPIFormDataMarker
from xpresso._openapi_providers.body.form_field import OpenAPIFormFieldMarker
from xpresso._openapi_providers.body.json import OpenAPIJsonMarker
from xpresso._openapi_providers.params.cookie import OpenAPICookieParameterMarker
from xpresso._openapi_providers.params.header import OpenAPIHeaderParameterMarker
from xpresso._openapi_providers.params.path import OpenAPIPathParameterMarker
from xpresso._openapi_providers.params.query import OpenAPIQueryParameterMarker
from xpresso.openapi import models as openapi_models

T = typing.TypeVar("T")

Example = typing.Union[openapi_models.Example, typing.Any]


def QueryParam(
    *,
    alias: typing.Optional[str] = None,
    style: openapi_models.QueryParamStyles = "form",
    explode: bool = True,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
    deprecated: typing.Optional[bool] = None,
) -> param_dependants.ParameterDependantMarker:
    extractor = QueryParameterExtractorMarker(
        alias=alias,
        explode=explode,
        style=style,
    )
    openapi = OpenAPIQueryParameterMarker(
        alias=alias,
        description=description,
        style=style,
        explode=explode,
        examples=examples,
        deprecated=deprecated,
    )
    return param_dependants.ParameterDependantMarker(
        in_="query",
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def PathParam(
    *,
    alias: typing.Optional[str] = None,
    style: openapi_models.PathParamStyles = "simple",
    explode: bool = False,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
    deprecated: typing.Optional[bool] = None,
) -> param_dependants.ParameterDependantMarker:
    extractor = PathParameterExtractorMarker(
        alias=alias,
        explode=explode,
        style=style,
    )
    openapi = OpenAPIPathParameterMarker(
        alias=alias,
        description=description,
        style=style,
        explode=explode,
        examples=examples,
        deprecated=deprecated,
    )
    return param_dependants.ParameterDependantMarker(
        in_="path",
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def HeaderParam(
    *,
    convert_underscores: bool = True,
    alias: typing.Optional[str] = None,
    explode: bool = False,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
    deprecated: typing.Optional[bool] = None,
) -> param_dependants.ParameterDependantMarker:
    extractor = HeaderParameterExtractorMarker(
        alias=alias,
        explode=explode,
        convert_underscores=convert_underscores,
    )
    openapi = OpenAPIHeaderParameterMarker(
        alias=alias,
        description=description,
        explode=explode,
        style="simple",
        examples=examples,
        deprecated=deprecated,
    )
    return param_dependants.ParameterDependantMarker(
        in_="header",
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def CookieParam(
    *,
    alias: typing.Optional[str] = None,
    explode: bool = True,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
    deprecated: typing.Optional[bool] = None,
) -> param_dependants.ParameterDependantMarker:
    extractor = CookieParameterExtractorMarker(
        alias=alias,
        explode=explode,
    )
    openapi = OpenAPICookieParameterMarker(
        alias=alias,
        description=description,
        style="form",
        explode=explode,
        examples=examples,
        deprecated=deprecated,
    )
    return param_dependants.ParameterDependantMarker(
        in_="cookie",
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def Json(
    *,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
    decoder: Decoder = json.loads,
    enforce_media_type: bool = True,
) -> param_dependants.BodyDependantMarker:
    extractor = JsonBodyExtractorMarker(
        decoder=decoder,
        enforce_media_type=enforce_media_type,
    )
    openapi = OpenAPIJsonMarker(
        description=description,
        examples=examples,
    )
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def File(
    *,
    media_type: typing.Optional[str] = None,
    enforce_media_type: bool = True,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
    format: Literal["binary", "base64"] = "binary",
) -> param_dependants.BodyDependantMarker:
    extractor = FileBodyExtractorMarker(
        media_type=media_type,
        enforce_media_type=enforce_media_type,
    )
    openapi = OpenAPIFileMarker(
        description=description,
        examples=examples,
        media_type=media_type,
        format=format,
    )
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def FormEncodedField(
    *,
    alias: typing.Optional[str] = None,
    style: openapi_models.FormDataStyles = "form",
    explode: bool = True,
) -> param_dependants.BodyDependantMarker:
    extractor = FormFieldBodyExtractorMarker(
        alias=alias,
        style=style,
        explode=explode,
    )
    openapi = OpenAPIFormFieldMarker(
        alias=alias,
        style=style,
        explode=explode,
    )
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def FormField(
    *,
    alias: typing.Optional[str] = None,
) -> param_dependants.BodyDependantMarker:
    extractor = FieldExtractorMarker(alias=alias)
    openapi = OpenAPIFieldMarker(alias=alias)
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def RepeatedFormField(
    *,
    alias: typing.Optional[str] = None,
) -> param_dependants.BodyDependantMarker:
    extractor = RepeatedFieldExtractorMarker(alias=alias)
    openapi = OpenAPIRepeatedFieldMarker(alias=alias)
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def Form(
    *,
    enforce_media_type: bool = True,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
) -> param_dependants.BodyDependantMarker:
    extractor = FormDataBodyExtractorMarker(
        enforce_media_type=enforce_media_type,
    )
    openapi = OpenAPIFormDataMarker(
        description=description,
        examples=examples,
        media_type="application/x-www-form-urlencoded",
    )
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def Multipart(
    *,
    enforce_media_type: bool = True,
    examples: typing.Optional[typing.Dict[str, Example]] = None,
    description: typing.Optional[str] = None,
) -> param_dependants.BodyDependantMarker:
    extractor = MultipartBodyExtractorMarker(
        enforce_media_type=enforce_media_type,
    )
    openapi = OpenAPIFormDataMarker(
        description=description,
        examples=examples,
        media_type="multipart/form-data",
    )
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


def ContentTypeDiscriminatedBody(
    *,
    description: typing.Optional[str] = None,
) -> param_dependants.BodyDependantMarker:
    extractor = ContentTypeDiscriminatedExtractorMarker()
    openapi = OpenAPIContentTypeDiscriminatedMarker(
        description=description,
    )
    return param_dependants.BodyDependantMarker(
        extractor_marker=extractor,
        openapi_marker=openapi,
    )


# Convenience type aliases
FromQuery = Annotated[T, QueryParam()]
FromHeader = Annotated[T, HeaderParam()]
FromCookie = Annotated[T, CookieParam()]
FromPath = Annotated[T, PathParam()]
FromJson = Annotated[T, Json()]
FromFile = Annotated[T, File()]
FromFormField = Annotated[T, FormEncodedField()]
ExtractField = Annotated[T, FormField()]
ExtractRepeatedField = Annotated[T, RepeatedFormField()]
FromFormData = Annotated[T, Form()]
FromMultipart = Annotated[T, Multipart()]
ByContentType = Annotated[T, ContentTypeDiscriminatedBody()]
