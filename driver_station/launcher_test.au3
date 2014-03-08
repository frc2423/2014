;
; Utility AutoIt script to launch the dashboard
;
; -> The FRC Driver Station will only launch predetermined executable files,
;    so to get around this we compile this AutoIt script to an exe, and we
; 	 put it in the right spot (c:\Program Files\FRC Dashboard\dashboard.exe),
;    then this dashboard program gets launched whenever the driver station
;    is launched.
;

$python = "C:\Python27\python27.exe"
;$python = "C:\Python27\pythonw27.exe"
$dir = "./"
$options = "--robot-ip 127.0.0.1  --no-cam --competition"

; We use GStreamer for PyGTK, so setup the environment correctly to use it
$sdkdir = EnvGet("GSTREAMER_SDK_ROOT_X86")
$oldpath = EnvGet("PATH")

EnvSet("PYTHONPATH", $sdkdir & "\lib\python2.7\site-packages")
EnvSet("PATH", $sdkdir & "\bin;" & $oldpath)

Run($python & " " & $dir & "\main.py " & $options, $dir)
