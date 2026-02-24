# TODO: remove the debuggin stuff
import pytest
import os
import sys #  DEBUG
from datetime import date
from pathlib import Path
import pprint # DEBUG

# from ganga.GangaCore.Utility.Deprecation import (
from GangaCore.Utility.Deprecation import ( # DEBUG
    extract_deprecation_info,
    find_deprecated_refs,
    DeprecationNotice
)

# TODO: Test: Find all instances in a directory
# TODO: Test: Don't include commented out sections
# TODO: Test: Find all classes
# TODO: Test: Find all functions
# TODO: Test: Find all async functions
# TODO: Test: Find deprecations that are not mandatory
def print_dbg (s):
    print (s)

file_path = Path (__file__)
root = file_path.parent.parent.parent.parent
testdir = root / "testdir/"

test_files_names = ["f1.py", "f2.py"]
test_files_paths = [testdir / name for name in test_files_names]
test_files_content = [
"""
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
""",
"""
from datetime import date
from GangaCore.Utility.Deprecation import (
    deprecation_deadline, deprecated
)
from typing_extensions import deprecated

# @deprecation_deadline(expires_on=date(2025, 12, 31), version="8.4.4")
# @deprecated ("MyDeprecatedClass deprecation reason")
# class MySecondDeprecatedClass:
#     pass

@deprecation_deadline(expires_on=date(2025, 12, 31), version="8.4.4")
@deprecated ("myAsyncFunc deprecation reason")
async def myFunc ():
    pass
"""
]

expected_report = [
    DeprecationNotice(
        name='MyDeprecatedClass',
        type='class',
        file_path='f1.py',
        lineno=11,
        reason='MyDeprecatedClass deprecation reason',
        deadline=date(2025, 12, 31),
        last_version='8.4.4'
    ),
   DeprecationNotice(
       name='myAsyncFunc',
       type='function',
       file_path='f1.py',
       lineno=16,
       reason='myAsyncFunc deprecation reason',
       deadline=date(2025, 12, 31), last_version='8.4.4'
   ),
   DeprecationNotice(
       name='myFunc',
       type='function',
       file_path='f2.py',
       lineno=15,
       reason='myAsyncFunc deprecation reason',
       deadline=date(2025, 12, 31),
       last_version='8.4.4'
   )
]

def test_deprecation_report_utils ():
    os.mkdir (testdir)
    for i in range (0, 2):
        with open (test_files_paths [i], "w") as f:
            f.write (test_files_content [i])
            # ...

    rr = find_deprecated_refs(testdir)
    dd = extract_deprecation_info (rr,testdir)


    assert dd == expected_report, "the produced report is inconsistent"

    for i in range (0, 2):
        test_files_paths [i].unlink ()


    os.rmdir (testdir)


