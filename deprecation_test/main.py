from datetime import date
from GangaCore.Utility.Deprecation import (
    deprecation_deadline, deprecated
)
from typing_extensions import deprecated


@deprecation_deadline(expires_on=date(2025, 12, 31), version="8.4.4")
@deprecated ("MyDeprecatedClass deprecation reason")
class MyDeprecatedClass:
    pass

@deprecation_deadline(expires_on=date(2025, 12, 31), version="8.4.4")
@deprecated ("myAsyncFunc deprecation reason")
async def myAsyncFunc ():
    pass


# test_directory = Path ("../../deprecation_test")
# rr = find_deprecated_refs(test_directory)
# dd = extract_deprecation_info (rr,test_directory)
#
# @deprecation_deadline(expires_on=date(2025, 12, 31), version="8.4.4")
# @deprecated ("myAsyncFunc deprecation reason")
# async def myAsyncFunc ():
#     pass
