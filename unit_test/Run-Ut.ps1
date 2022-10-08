$utDir = $PSScriptRoot
$npmDir = 'C:\Users\Brend\OneDrive\Documents\demo\npm\node_modules\trapit\'
$utOutFiles = @('trapit_py_out.json')

sl $utDir
'Executing:  py testtrapit.py at ' + (Date -format "dd-MMM-yy HH:mm:ss")
py testtrapit.py

'Format the unit test results from folder: ' + $npmDir + "`n"

sl $npmDir
Foreach($f in $utOutFiles) {
    $jsonFile = ($utDir + '\' + $f)
    ('Copying ' + $jsonFile + ' to .\externals\python')
    cp $jsonFile .\externals\python
}
node externals\format-externals python > python.log
cat .\python.log