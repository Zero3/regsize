# regsize
Python script for finding the largest Windows registry subkeys.

The size of each subkey is calculated by summing the number of characters in:
- The name of the subkey
- The names of the values in the subkey
- The data of the values in the subkey when converted to strings

## Usage
`regsize.py`

## Settings
By default, the script will scan the paths `HKEY_LOCAL_MACHINE\SOFTWARE` and `HKEY_CURRENT_USER` and report back any subkey paths whose size exceeds 10% of the total size of all scanned paths.

These settings can be changed at the bottom of the script.

## Example
````
> python regsize.py
Scanned paths [17,997,091]
|
+--HKEY_LOCAL_MACHINE\SOFTWARE [9,532,902]
|  |
|  +--Microsoft [6,372,099]
|  |  |
|  |  +--.NETFramework [3,408,791]
|  |     |
|  |     +--v2.0.50727 [3,392,612]
|  |        |
|  |        +--NGENService [3,392,576]
|  |           |
|  |           +--Roots [3,392,490]
|  |
|  +--Classes [3,104,152]
|
+--HKEY_CURRENT_USER [8,464,189]
   |
   +--Software [8,387,967]
      |
      +--Classes [5,856,053]
         |
         +--Local Settings [5,825,768]
            |
            +--Software [5,751,265]
               |
               +--Microsoft [5,751,257]
                  |
                  +--Windows [5,751,248]
                     |
                     +--Shell [3,200,617]
                     |
                     +--CurrentVersion [2,550,016]
                        |
                        +--TrayNotify [2,549,860]
````
