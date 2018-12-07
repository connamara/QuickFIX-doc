*** Settings ***
Documentation    Acceptance tests for QuickFIX-doc
Library          OperatingSystem
Library          Collections

*** Variables ***
${specdir}       /tmp/quickfix/spec/
${specvar}       FIXSPECNAME

*** Test Cases ***
Generate FIX Specs and Compare Outputs
    [Setup]    Environment Variable Should Be Set    ${specvar}
    ${specname} =    Get Environment Variable    ${specvar}
    Log to Console    ${specname}
    @{files} =    List Directory    /opt/python/
    ${lastoutdir} =    Set Variable    ${EMPTY}
    :FOR    ${pyinst}    IN    @{files}
    \    ${outdir} =    Set Variable    /tmp/specgen/${pyinst}/${specname}
    \    ${process} =    Set Variable    /opt/python/${pyinst}/bin/python -m quickfix_doc ${specdir}/${specname}.xml ${outdir}
    \    Log to Console    Executing: ${process}
    \    ${rc}    ${output} =    Run and Return RC and Output    ${process}
    \    Log    ${output}
    \    Should Be Equal As Integers    ${rc}    0
    \    File Should Not Be Empty    ${outdir}/html/index.html
    \    Run Keyword If    len($lastoutdir) > 0    Compare Generated Spec Outputs    ${outdir}    ${lastoutdir}
    \    ${lastoutdir} =    Set Variable    ${outdir}

*** Keywords ***
Compare Generated Spec Outputs
    [Arguments]    ${spec1}    ${spec2}
    Perform Diff    ${spec1}/index.rst    ${spec2}/index.rst
    @{files1} =    List Directory    ${spec1}/Messages
    Should Not Be Empty    ${files1}
    @{files2} =    List Directory    ${spec2}/Messages
    Should Not Be Empty    ${files2}
    Sort List    ${files1}
    Sort List    ${files2}
    Lists Should Be Equal    ${files1}    ${files2}
    :FOR    ${msgfile}    IN    @{files1}
    \    Perform Diff    ${spec1}/Messages/${msgfile}    ${spec2}/Messages/${msgfile}

Perform Diff
    [Arguments]    ${file1}    ${file2}
    File Should Not Be Empty    ${file1}
    File Should Not Be Empty    ${file2}
    ${diffexec} =    Set Variable    diff "${file1}" "${file2}"
    ${rc}    ${output} =    Run and Return RC and Output    ${diffexec}
    Run Keyword Unless    ${rc} == 0    Fail    ${diffexec}:\n${output}
