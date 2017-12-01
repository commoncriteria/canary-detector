Usage
=====

## Dependencies
Cande is a Python 3 script that depends on objdump;
therefore, it is necessary to install Python 3 and objdump before using it.

## Running
Cande is invoked in the following way:
   cande [-v] &lt;executable-file-1> [ &lt;executable-file-2> [...]]

-t : _(T)horough_ mode. Normally cande exits once it detects a single stack-canary. In _thorough_ mode, it attempts to find all stack-canaries

&lt;executable-file-X>: These are native binaries that are either Microsoft's Portable Executable (PE) type(both Dynamically Linked Libraries and Executables) or the Executable and Linkable Format type that exist on Unix-derivative systems (this includes shared libraries, *.so, files).

If a canary is found, cande prints
>   Found gcc-style canary in '...'

or
>   Found ms-style canary in '...'

If no canaries are found, no messages are displayed.
