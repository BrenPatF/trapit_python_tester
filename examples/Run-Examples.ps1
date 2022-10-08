$examplesDir = $PSScriptRoot
$npmDir = 'C:\Users\Brend\OneDrive\Documents\demo\npm\node_modules\trapit\'
$examples = @('colgroup', 'helloworld')
$examplesOutFiles = @('colgroup\colgroup_out.json', 'helloworld\helloworld_out.json')

sl $examplesDir
Foreach($e in $examples) {
    Foreach($tp in @('main', 'test')) {
        $prog = $e + '\' + $tp + $e + '.py'
        "Executing:  py $prog at " + (Date -format "dd-MMM-yy HH:mm:ss")
        py $prog
    }
}
'Format the unit test results from folder: ' + $npmDir + "`n"
sl $npmDir
Foreach($f in $examplesOutFiles) {
    $jsonFile = ($examplesDir + '\' + $f)
    ('Copying ' + $jsonFile + ' to .\externals\python')
    cp $jsonFile .\externals\python
}
node externals\format-externals python > python.log
cat .\python.log