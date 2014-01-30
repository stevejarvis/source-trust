SourceTrust
==========

About
-----
SourceTrust as in not trustworthy. It's a demonstration of Ken Thompson's
presentation "[Reflections on Trusting Trust]
(http://cm.bell-labs.com/who/ken/trust.html)".

This is a proof of concept with emulated compiling and binaries using Python.
The source code of the compiler is compiler.py, the app is login_app.py.
Binaries are the marshal'd code objects representing these files, and can
be executed with runner.py.

Steps
-----
* Compile the compiler
Initially, login_app.py works as expected. "please" is accepted and "backdoor"
denied.
    ./compiler.py compiler.py
    ./runner.py compiler.marshal login_app.py
    ./runner.py login_app.marshal please    # accepted
    ./runner.py login_app.marshal backdoor    # denied

* Enable the step 2 code and re-compile the compiler (with the compiler).
At this point, there's is obvious malicious code in the compiler and the
malicious user can be granted access to the application. "backdoor" is
accepted as a password.
    ./runner.py compiler.marshal compiler.py
    ./runner.py compiler.marshal login_app.py
    ./runner.py login_app.marshal please    # accepted
    ./runner.py login_app.marshal backdoor    # accepted
Note: This step is not actually necessary to get the final effect.

* Disable the step 2 code and enable step 3 code. Recompile the compiler.
The step 3 substitution is targeted at the compiler, to introduce the
bug from step 2 and re-insert itself during the compiler's compilation.
    ./runner.py compiler.marshal compiler.py

Now the bug is in the compiler binary (compiler.marshal). Every time that
binary is used to compile compiler.py, it will reintroduce the bugs into the
compiler, and ultimately into the login application, even after the there is
no presence of the malicious code in the source.
    ./runner.py compiler.marshal login_app.py
    ./runner.py login_app.marshal please    # accepted
    ./runner.py login_app.marshal backdoor    # accepted (no, see notes)

* Disable all the shady code, re-compile the compiler and use it to re-compile
the login_app. There is no malicious code in the source, yet the bug persists.
    ./runner.py compiler.marshal compiler.py
    ./runner.py compiler.marshal login_app.py
    ./runner.py login_app.marshal please    # accepted
    ./runner.py login_app.marshal backdoor    # accepted


Notes and (Unintentional) Bugs
----------------------------

There's room for improvement, but I believe this suffices to be an interesting
example.

What particularly needs work:
* The self-replicating code is not awesome. It degrades in such a way that it
persists just long enough to complete the aforementioned steps. A quality
example would replicate that section of code verbatim (see
[quine](http://en.wikipedia.org/wiki/Quine_(computing))).

* The bug is actually not directly introduced upon first compilation with the
bugged compiler, only the bug to later replicate. So the backdoor will be
introduced to login_app after the second generation.