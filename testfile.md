## InvalidTargetException
_class InvalidTargetException(Exception):_

XXX

|extends|description|
|---|---|
|Exception|XXX|

## \_\_init\_\_()
_def \_\_init\_\_(self, source, target):_

XXX

|param|description|
|---|---|
|self|XXX|
|source|XXX|
|target|XXX|

__returns:__ _None_
## UnexpectedValueException
_class UnexpectedValueException(Exception):_

XXX

|extends|description|
|---|---|
|Exception|XXX|

## \_\_init\_\_()
_def \_\_init\_\_(self, item):_

XXX

|param|description|
|---|---|
|self|XXX|
|item|XXX|

__returns:__ _None_
## UnknownPlatformException
_class UnknownPlatformException(Exception):_

XXX

|extends|description|
|---|---|
|Exception|XXX|

## \_\_init\_\_()
_def \_\_init\_\_(self, platform):_

XXX

|param|description|
|---|---|
|self|XXX|
|platform|XXX|

__returns:__ _None_
## UnknownShellException
_class UnknownShellException(Exception):_

XXX

|extends|description|
|---|---|
|Exception|XXX|

## \_\_init\_\_()
_def \_\_init\_\_(self, shell):_

XXX

|param|description|
|---|---|
|self|XXX|
|shell|XXX|

__returns:__ _None_
## get\_platform()
_def get\_platform() -> int:_

XXX

__returns:__ _int_:&nbsp; XXX
## str\_stat()
_def str\_stat(p: int) -> str:_

XXX

|param|description|
|---|---|
|p: int|XXX|

__returns:__ _str_:&nbsp; XXX
## win\_or\_linux()
_def win\_or\_linux() -> int:_

XXX

__returns:__ _int_:&nbsp; XXX
## win\_lstrip()
_def win\_lstrip(text: str) -> str:_

XXX

|param|description|
|---|---|
|text: str|XXX|

__returns:__ _str_:&nbsp; XXX
## win\_rstrip()
_def win\_rstrip(text: str) -> str:_

XXX

|param|description|
|---|---|
|text: str|XXX|

__returns:__ _str_:&nbsp; XXX
## win\_strip()
_def win\_strip(text: str) -> str:_

XXX

|param|description|
|---|---|
|text: str|XXX|

__returns:__ _str_:&nbsp; XXX
## win\_default\_shell()
_def win\_default\_shell() -> int:_

XXX

__returns:__ _int_:&nbsp; XXX
## shell()
_def shell(target: int, args: List, tab=False, verbose=False, strip=True, win\_remove\_carriage=True) -> str:_

XXX

|param|description|
|---|---|
|target: int|XXX|
|args: List|XXX|
|tab=False|XXX|
|verbose=False|XXX|
|strip=True|XXX|
|win\_remove\_carriage=True|XXX|

__returns:__ _str_:&nbsp; XXX
## windows()
_def windows(args: List, tab=False, verbose=False) -> str:_

XXX

|param|description|
|---|---|
|args: List|XXX|
|tab=False|XXX|
|verbose=False|XXX|

__returns:__ _str_:&nbsp; XXX
## cmd()
_def cmd(args: List, tab=False, verbose=False) -> str:_

XXX

|param|description|
|---|---|
|args: List|XXX|
|tab=False|XXX|
|verbose=False|XXX|

__returns:__ _str_:&nbsp; XXX
## powershell()
_def powershell(args: List, tab=False, verbose=False) -> str:_

XXX

|param|description|
|---|---|
|args: List|XXX|
|tab=False|XXX|
|verbose=False|XXX|

__returns:__ _str_:&nbsp; XXX
## wsl()
_def wsl(args: List, tab=False, verbose=False) -> str:_

XXX

|param|description|
|---|---|
|args: List|XXX|
|tab=False|XXX|
|verbose=False|XXX|

__returns:__ _str_:&nbsp; XXX
## linux()
_def linux(args: List, tab=False, verbose=False) -> str:_

XXX

|param|description|
|---|---|
|args: List|XXX|
|tab=False|XXX|
|verbose=False|XXX|

__returns:__ _str_:&nbsp; XXX
## is\_alpha()
_def is\_alpha(text: str, extra: List = None) -> bool:_

XXX

|param|description|
|---|---|
|text: str|XXX|
|extra: List = None|XXX|

__returns:__ _bool_:&nbsp; XXX
## env()
_def env(target: int, var\_name: str, cmd\_logic=True) -> str:_

XXX

|param|description|
|---|---|
|target: int|XXX|
|var\_name: str|XXX|
|cmd\_logic=True|XXX|

__returns:__ _str_:&nbsp; XXX
## wenv()
_def wenv(var\_name: str) -> str:_

XXX

|param|description|
|---|---|
|var\_name: str|XXX|

__returns:__ _str_:&nbsp; XXX
## lenv()
_def lenv(var\_name: str) -> str:_

XXX

|param|description|
|---|---|
|var\_name: str|XXX|

__returns:__ _str_:&nbsp; XXX
## denv()
_def denv(var\_name: str) -> str:_

XXX

|param|description|
|---|---|
|var\_name: str|XXX|

__returns:__ _str_:&nbsp; XXX
