# Automatic COM Registration Checker

This NVDA add-on, periodically checks that the system's COM registrations needed for accessibility of Windows and many applications, have not been damaged and have not gone missing, as sometimes happens.

It is a proof of concept for a proposal which will be submitted to NV Access for inclusion in NVDA core.

If the add-on detects that your COM registrations have become corrupted in some way, it will pop up a window suggesting that you run NVDA's COM Registration Fixing Tool.
It will provide a button to do so.

It checks for changes to the COM registrations at NVDA start, and every five minutes thereafter.

This add-on has no user serviceable parts.
Just set it and forget it.
