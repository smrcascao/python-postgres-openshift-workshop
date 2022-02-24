{{- define "microService.name" -}}
{{- printf "%s-%s" .Values.global.appName .Chart.Name | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "namespace" -}}
{{- include "microService.name" . -}}
{{- end }}

{{- define "container.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "container" -}}
{{- end }}

{{- define "deployment.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "deployment" -}}
{{- end }}

{{- define "horizontalpodautoscaler.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "hpa" -}}
{{- end }}

{{- define "ingress.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "ingress" -}}
{{- end }}

{{- define "service.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "svc" -}}
{{- end }}

{{- define "serviceproviderclass.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "serviceproviderclass" -}}
{{- end }}

{{- define "secret.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "secret" -}}
{{- end }}

{{- define "volume.name" -}}
{{- printf  "%s-%s" ((include "microService.name" . )) "volume" -}}
{{- end }}