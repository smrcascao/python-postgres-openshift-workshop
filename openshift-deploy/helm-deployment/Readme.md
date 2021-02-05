# Dependences

## Install SOPS

[Howt to install SOPS](https://github.com/mozilla/sops)

## Intall Helm 

[How to install Helm 3](https://helm.sh/docs/intro/install/)

## Intall helm-secrets Plugin

[How to install helm-secrets](https://github.com/jkroepke/helm-secrets)

## Intall GPG

[How to install GPG](https://gnupg.org/download/)

---

## To create a key (passphrase "secret") superteam@criticaltechworks.com
``` gpg --gen-key ```

## To export a public key into file public.key:
``` gpg --export -a "superteam@criticaltechworks.com" > public.key ```

## To export a private key:
``` gpg --export-secret-key -a "superteam@criticaltechworks.com" > private.key```

## To import private key:
``` gpg --import private.key ```

## List your public key with the following command:
``` gpg --fingerprint superteam@criticaltechworks.com ```

output:

``` bash 
pub   rsa2048 2021-02-01 [SC]
      A929 6F1F D1BC C629 2FA0  1792 FA05 9094 E45E 39AE
uid           [ultimate] super team (secrets) <superteam@criticaltechworks.com>
sub   rsa2048 2021-02-01 [E]
```

## Export  env "**SOPS_PGP_FP**"
```export SOPS_PGP_FP="A9296F1FD1BCC6292FA01792FA059094E45E39AE" ```

## Create .sops.yaml file in the same directory you have your values.yaml file

.sops.yaml
``` bash 

creation_rules:
-- pgp: ‘A929 6F1F D1BC C629 2FA0  1792 FA05 9094 E45E 39AE’
encrypted_suffix: ‘Secret’
```
**encrypted_suffix** means the key you want to encrypt in **values**.yaml file should have Secret prefix.
For eg. mongoPasswordSecret, serviceBusSecret etc.

## Create a chart example
``` heml create openshift-workshop  ```

## Encrypt secrets
```helm secrets enc values.secrets.yaml ```

## Decrypt secrets
```helm secrets dec values.secrets.yaml ```


## Check if your chart is fine
``` helm secrets lint --values values.secrets.yaml ```

**--values (or -f)**: Specify a YAML file with overrides. This can be specified multiple times and the rightmost file will take precedence.
More info [here](https://helm.sh/docs/helm/helm_install/).

## Check variables values in your yaml

``` helm secrets template . --values values.secrets.yaml ```

## Install Helm chart
``` helm secrets  install openshift-workshop . --values values.secrets.yaml ```

## List all installed charts
``` helm ls ```

## Remove Helm chart
``` helm uninstall openshift-workshop  ```
