

# The CEDAR Web App
 
Authors: Brennan Chapman ([@chapb](https://github.com/chapb)) and Charly Phillips ([@phillipsclynn](https://github.com/phillipsclynn))



See [Internal Documentation](https://github.com/iAM-AMR/internal-documentation). 


## Set environment variables

### Powershell

Where .env is path to env file.

```
switch -File .env {
    default {
      $name, $value = $_.Trim() -split '=', 2
      if ($name -and $name[0] -ne '#') { # ignore blank and comment lines.
        Set-Item "Env:$name" $value
      }
    }
  }
```
