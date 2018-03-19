# Red Team Automation (RTA)

RTA provides a framework of scripts designed to allow blue teams to test their detection capabilities against malicious tradecraft, modeled after [MITRE ATT&CK](https://attack.mitre.org/wiki/ATT&CK_Matrix).

RTA is composed of python scripts that generate evidence of over 50 different ATT&CK tactics, as well as a compiled binary application that performs activities such as file timestopping, process injections, and beacon simulation as needed.

Where possible, RTA attempts to perform the actual malicious activity describe. In other cases, the RTAs will emulate all or parts of the activity. For example, some lateral movement will by default target local host (though with parameters typically allow for multi-host testing).  In other cases, executables such as cmd.exe or python.exe will be renamed to make it appeas as if a Windows binary is doing non-standard activities.

# Installation

## Prerequisites
 * Python2.7


## Installation Steps
1) Download a copy of the RTA repo from https://git.endgames.local/RnD/rta.
2) Extract the contents of the zip archive into an RTA folder, such as c:\RTA  
3) For the full experience, download additional files into the bin subdirectory (as described in the dependencies section below)

## Dependencies
Some of the RTAs require 3rd party tools in order to execute properly. You can run many RTAs without additional tools, but to make use of the full suite, some will require additional downloads.

The following table provides dependency information:

| Dependency | RTAs | source |
| ---        | ---  | ---    |
| Sysinternals Suite | user_dir_escalation.py, sip_provider.py, system_restore_proc.py, trust_provider.py | [Microsoft](https://docs.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) |
| MsXsl              | msxsl_network.py | [Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=21714) |


## Other Considerations
Windows Defender or other Anti-Virus products may block or otherwise interfere with RTAs while they run. Consider how you configure security products on the test host before running RTAs based on the goals of your tests.

## Customization
By modifying common.py, you can customize how RTA scripts will work in your environment. You could even write an entirely new function for use in one or more new RTAs.

# Running RTAs
To run the `powershell_args.py` RTA, simply run:
```commandline
python powershell_args.py
```

To run an entire directory of RTAs, you can use a loop:

**Windows:**
```commandline
for %f in (*.py) do python %f
```

**Linux/Mac:**
```commandline
for i in (*.py); do python $i; done
```

None of the rules require arguments, but some can optionally take arguments for further customization of the technique.

# FAQ
To help with common issues, please refer to the following frequently-asked questions:

* When I run some RTA scripts, I get an error that "PsExec" can't be found

To resolve errors about a missing dependency, please make sure that you've followed instructions to download third-party utilities such as the Sysinternals suite and that you've extracted these executables to the "bin" subdirectory.

* I attempted to use the lateral_command.py script in an environment where at least one other workstation was found, but the script is throwing errors about RPC access

Your environment may have host-based firewalls that are preventing you from moving laterally. This is a great thing that you should not disable in production! Instead, note whether or not you can detect the failed attempt.

* When I run some RTA scripts, I get an error that "Access is denied"

When Windows defender or other AV products detect malicious activity, sometimes will lock files resulting in this error. Consult your AV logs to see if that is the reason for the error.
 
* I noticed that there isn't a script for MITRE technique TXXXX - when's that coming?
 
Endgame will continue to release scripts in the coming weeks and months which correspond to various MITRE ATT&CK techniques. If you've already written a script, we're accepting pull requests and will gladly review and merge additions! Contributing to this repository is a great way to extend RTA for the entire community.
