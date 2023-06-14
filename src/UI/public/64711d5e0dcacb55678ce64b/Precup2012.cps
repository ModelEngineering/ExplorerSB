<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.24 (Build 197) (http://www.copasi.org) at 2019-08-19 15:09:18 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="24" versionDevel="197" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#Function_13">
   <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000163" />
   </rdf:Description>
   </rdf:RDF>
      </MiriamAnnotation>
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
<b>Mass action rate law for irreversible reactions</b>
<p>
Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does not include any reverse process that creates the reactants from the products. The change of a product quantity is proportional to the quantity of one reactant.
</p>
</body>
      </Comment>
      <Expression>
        k1*PRODUCT&lt;substrate_i>
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_80" name="k1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_81" name="substrate" order="1" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function_for_Normal_Cells_Growth" type="UserDefined" reversible="unspecified">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_43">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:22:02Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        (
a
)/(
1+b*(x+y+z)
)*(
(
x+y+epsilon
)/(
x+y+epsilon+g*z
)
)*x
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_281" name="x" order="0" role="product"/>
        <ParameterDescription key="FunctionParameter_275" name="a" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_262" name="b" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_280" name="y" order="3" role="modifier"/>
        <ParameterDescription key="FunctionParameter_284" name="z" order="4" role="modifier"/>
        <ParameterDescription key="FunctionParameter_286" name="epsilon" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_288" name="g" order="6" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function_for_Leukemic_Cells_Growth" type="UserDefined" reversible="unspecified">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_45">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:26:28Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        (
A
)/(
1+B*(x+y+z)
)*(
(
x+y+epsilon
)/(
x+y+epsilon+G*z
)
)*y
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_282" name="A" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_287" name="B" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_306" name="x" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_279" name="y" order="3" role="product"/>
        <ParameterDescription key="FunctionParameter_303" name="z" order="4" role="modifier"/>
        <ParameterDescription key="FunctionParameter_301" name="epsilon" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_299" name="G" order="6" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function_for_Donor_Cells_Growth" type="UserDefined" reversible="unspecified">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_49">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:31:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        (
(
a
)/(
1+b*(x+y+z)
)
)*(
1-(
(
h*(x+y)
)/(
z+epsilon+h*(x+y)
)
)
)*z
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_278" name="a" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_269" name="b" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_268" name="x" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_302" name="y" order="3" role="modifier"/>
        <ParameterDescription key="FunctionParameter_319" name="z" order="4" role="product"/>
        <ParameterDescription key="FunctionParameter_317" name="h" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_315" name="epsilon" order="6" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_1" name="Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation" simulationType="time" timeUnit="d" volumeUnit="ml" areaUnit="m²" lengthUnit="m" quantityUnit="#" type="deterministic" avogadroConstant="6.0221408570000002e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_1">
    <bqbiol:hasProperty rdf:resource="urn:miriam:mamo:MAMO_0000046"/>
    <bqbiol:hasProperty rdf:resource="urn:miriam:ncit:C3161"/>
    <bqbiol:hasProperty rdf:resource="urn:miriam:ncit:NCIT:C46089"/>
    <dcterms:bibliographicCitation>
      <rdf:Description>
        <CopasiMT:isDescribedBy rdf:resource="urn:miriam:doi:10.1142/S1793524511001684"/>
      </rdf:Description>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:12:47Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Description>
        <vCard:EMAIL>johannes.p.meyer@gmail.com</vCard:EMAIL>
        <vCard:N>
          <rdf:Description>
            <vCard:Family>Meyer</vCard:Family>
            <vCard:Given>Johannes</vCard:Given>
          </rdf:Description>
        </vCard:N>
        <vCard:ORG>
          <rdf:Description>
            <vCard:Orgname>EMBL-EBI</vCard:Orgname>
          </rdf:Description>
        </vCard:ORG>
      </rdf:Description>
    </dcterms:creator>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      This is a basic mathematical model describing the dynamics of three cell lines (normal host cells, leukemic host cells and donor cells) after allogeneic stem cell transplantation.
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_0" name="compartment" simulationType="fixed" dimensionality="3" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_0">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:59:57Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is rdf:resource="urn:miriam:bto:BTO:0000141"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_0" name="x" simulationType="reactions" compartment="Compartment_0" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_0">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:18:53Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:bto:BTO:0000725"/>
    <CopasiMT:occursIn rdf:resource="urn:miriam:bto:BTO:0000141"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_1" name="y" simulationType="reactions" compartment="Compartment_0" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_1">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:33:54Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is rdf:resource="urn:miriam:bto:BTO:0004178"/>
    <CopasiMT:occursIn rdf:resource="urn:miriam:bto:BTO:0000141"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_2" name="z" simulationType="reactions" compartment="Compartment_0" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_2">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:33:55Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:bto:BTO:0000725"/>
    <CopasiMT:occursIn rdf:resource="urn:miriam:bto:BTO:0000141"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_0" name="a" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_1" name="A" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_2" name="b" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_3" name="B" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_4" name="c" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_5" name="C" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_6" name="epsilon" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_7" name="g" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_8" name="G" simulationType="fixed" addNoise="false">
      </ModelValue>
      <ModelValue key="ModelValue_9" name="h" simulationType="fixed" addNoise="false">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_0" name="Normal_Cells_Growth" reversible="false" fast="false" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_0">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:20:07Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is rdf:resource="urn:miriam:go:GO:0071425"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_0" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_1" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_7565" name="a" value="0.23"/>
          <Constant key="Parameter_7560" name="b" value="2.2e-08"/>
          <Constant key="Parameter_7561" name="epsilon" value="1"/>
          <Constant key="Parameter_7562" name="g" value="2"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default" scalingCompartment="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="ModelValue_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_286">
              <SourceParameter reference="ModelValue_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="ModelValue_7"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="Normal_Cells_Removal" reversible="false" fast="false" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_1">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:26:02Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:go:GO:0035701"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_0" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_7512" name="k1" value="0.01"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_80">
              <SourceParameter reference="ModelValue_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Metabolite_0"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="Leukemic_Cells_Growth" reversible="false" fast="false" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_2">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:26:43Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:go:GO:0071425"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_0" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_7569" name="A" value="0.45"/>
          <Constant key="Parameter_7564" name="B" value="2.2e-08"/>
          <Constant key="Parameter_7568" name="epsilon" value="1"/>
          <Constant key="Parameter_7567" name="G" value="2"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default" scalingCompartment="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="ModelValue_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="ModelValue_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_306">
              <SourceParameter reference="Metabolite_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_303">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_301">
              <SourceParameter reference="ModelValue_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_299">
              <SourceParameter reference="ModelValue_8"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="Leukemic_Cells_Removal" reversible="false" fast="false" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_3">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:28:32Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:go:GO:0035701"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_7563" name="k1" value="0.01"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_80">
              <SourceParameter reference="ModelValue_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="Donor_Cells_Growth" reversible="false" fast="false" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_4">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:30:20Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:go:GO:0071425"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_0" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_7571" name="a" value="0.23"/>
          <Constant key="Parameter_7570" name="b" value="2.2e-08"/>
          <Constant key="Parameter_7573" name="h" value="2"/>
          <Constant key="Parameter_7572" name="epsilon" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default" scalingCompartment="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="ModelValue_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Metabolite_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_302">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_319">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_317">
              <SourceParameter reference="ModelValue_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_315">
              <SourceParameter reference="ModelValue_6"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="Donor_Cells_Removal" reversible="false" fast="false" addNoise="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_5">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2019-08-19T15:33:38Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf rdf:resource="urn:miriam:go:GO:0035701"/>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_7566" name="k1" value="0.01"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_80">
              <SourceParameter reference="ModelValue_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment]" value="1" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment],Vector=Metabolites[x]" value="200000000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment],Vector=Metabolites[y]" value="100000000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment],Vector=Metabolites[z]" value="400000000" type="Species" simulationType="reactions"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[a]" value="0.23000000000000001" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[A]" value="0.45000000000000001" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[b]" value="2.1999999999999998e-08" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[B]" value="2.1999999999999998e-08" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[c]" value="0.01" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[C]" value="0.01" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[epsilon]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[g]" value="2" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[G]" value="2" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[h]" value="2" type="ModelValue" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Growth]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Growth],ParameterGroup=Parameters,Parameter=a" value="0.23000000000000001" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[a],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Growth],ParameterGroup=Parameters,Parameter=b" value="2.1999999999999998e-08" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[b],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Growth],ParameterGroup=Parameters,Parameter=epsilon" value="1" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[epsilon],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Growth],ParameterGroup=Parameters,Parameter=g" value="2" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[g],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Removal]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Normal_Cells_Removal],ParameterGroup=Parameters,Parameter=k1" value="0.01" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Growth]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Growth],ParameterGroup=Parameters,Parameter=A" value="0.45000000000000001" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[A],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Growth],ParameterGroup=Parameters,Parameter=B" value="2.1999999999999998e-08" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[B],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Growth],ParameterGroup=Parameters,Parameter=epsilon" value="1" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[epsilon],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Growth],ParameterGroup=Parameters,Parameter=G" value="2" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[G],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Removal]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Leukemic_Cells_Removal],ParameterGroup=Parameters,Parameter=k1" value="0.01" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[C],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Growth]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Growth],ParameterGroup=Parameters,Parameter=a" value="0.23000000000000001" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[a],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Growth],ParameterGroup=Parameters,Parameter=b" value="2.1999999999999998e-08" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[b],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Growth],ParameterGroup=Parameters,Parameter=h" value="2" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[h],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Growth],ParameterGroup=Parameters,Parameter=epsilon" value="1" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[epsilon],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Removal]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Reactions[Donor_Cells_Removal],ParameterGroup=Parameters,Parameter=k1" value="0.01" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Values[c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_1"/>
      <StateTemplateVariable objectReference="Metabolite_0"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Metabolite_2"/>
      <StateTemplateVariable objectReference="Compartment_0"/>
      <StateTemplateVariable objectReference="ModelValue_0"/>
      <StateTemplateVariable objectReference="ModelValue_1"/>
      <StateTemplateVariable objectReference="ModelValue_2"/>
      <StateTemplateVariable objectReference="ModelValue_3"/>
      <StateTemplateVariable objectReference="ModelValue_4"/>
      <StateTemplateVariable objectReference="ModelValue_5"/>
      <StateTemplateVariable objectReference="ModelValue_6"/>
      <StateTemplateVariable objectReference="ModelValue_7"/>
      <StateTemplateVariable objectReference="ModelValue_8"/>
      <StateTemplateVariable objectReference="ModelValue_9"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 200000000 100000000 400000000 1 0.23000000000000001 0.45000000000000001 2.1999999999999998e-08 2.1999999999999998e-08 0.01 0.01 1 2 2 2 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_14" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="JacobianRequested" type="bool" value="1"/>
        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
      </Problem>
      <Method name="Enhanced Newton" type="EnhancedNewton">
        <Parameter name="Resolution" type="unsignedFloat" value="1.0000000000000001e-09"/>
        <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Use Newton" type="bool" value="1"/>
        <Parameter name="Use Integration" type="bool" value="1"/>
        <Parameter name="Use Back Integration" type="bool" value="0"/>
        <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
        <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
        <Parameter name="Maximum duration for forward integration" type="unsignedFloat" value="1000000000"/>
        <Parameter name="Maximum duration for backward integration" type="unsignedFloat" value="1000000"/>
      </Method>
    </Task>
    <Task key="Task_15" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="1000"/>
        <Parameter name="StepSize" type="float" value="0.80000000000000004"/>
        <Parameter name="Duration" type="float" value="800"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="9.9999999999999995e-07"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="9.9999999999999998e-13"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_16" name="Scan" type="scan" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="1"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_17" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_18" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_11" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <ParameterText name="ObjectiveExpression" type="expression">
          
        </ParameterText>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
      </Problem>
      <Method name="Random Search" type="RandomSearch">
        <Parameter name="Log Verbosity" type="unsignedInteger" value="0"/>
        <Parameter name="Number of Iterations" type="unsignedInteger" value="100000"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_19" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_12" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
        </ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
        </ParameterGroup>
      </Problem>
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Log Verbosity" type="unsignedInteger" value="0"/>
        <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
        <Parameter name="Stop after # Stalled Generations" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_14"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1.0000000000000001e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_21" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
        <Parameter name="DivergenceRequested" type="bool" value="1"/>
        <Parameter name="TransientTime" type="float" value="0"/>
      </Problem>
      <Method name="Wolf Method" type="WolfMethod">
        <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
        <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="9.9999999999999995e-07"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="9.9999999999999998e-13"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_22" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
      </Problem>
      <Method name="ILDM (LSODA,Deuflhard)" type="TimeScaleSeparation(ILDM,Deuflhard)">
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="0.0001"/>
      </Method>
    </Task>
    <Task key="Task_23" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_16" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
        <ParameterGroup name="TargetFunctions">
          <Parameter name="SingleObject" type="cn" value=""/>
          <Parameter name="ObjectListType" type="unsignedInteger" value="7"/>
        </ParameterGroup>
        <ParameterGroup name="ListOfVariables">
          <ParameterGroup name="Variables">
            <Parameter name="SingleObject" type="cn" value=""/>
            <Parameter name="ObjectListType" type="unsignedInteger" value="41"/>
          </ParameterGroup>
          <ParameterGroup name="Variables">
            <Parameter name="SingleObject" type="cn" value=""/>
            <Parameter name="ObjectListType" type="unsignedInteger" value="0"/>
          </ParameterGroup>
        </ParameterGroup>
      </Problem>
      <Method name="Sensitivities Method" type="SensitivitiesMethod">
        <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Delta minimum" type="unsignedFloat" value="9.9999999999999998e-13"/>
      </Method>
    </Task>
    <Task key="Task_24" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_25" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
        <Parameter name="LimitCrossings" type="bool" value="0"/>
        <Parameter name="NumCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitOutTime" type="bool" value="0"/>
        <Parameter name="LimitOutCrossings" type="bool" value="0"/>
        <Parameter name="PositiveDirection" type="bool" value="1"/>
        <Parameter name="NumOutCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitUntilConvergence" type="bool" value="0"/>
        <Parameter name="ConvergenceTolerance" type="float" value="9.9999999999999995e-07"/>
        <Parameter name="Threshold" type="float" value="0"/>
        <Parameter name="DelayOutputUntilConvergence" type="bool" value="0"/>
        <Parameter name="OutputConvergenceTolerance" type="float" value="9.9999999999999995e-07"/>
        <ParameterText name="TriggerExpression" type="expression">
          
        </ParameterText>
        <Parameter name="SingleVariable" type="cn" value=""/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="9.9999999999999995e-07"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="9.9999999999999998e-13"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_26" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_17" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value=""/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_9" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_11" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_13" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_16" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_17" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
      </Footer>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Precup2012_Figure_1_B" type="Plot2D" active="1" taskTypes="">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[x]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment],Vector=Metabolites[x],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[y]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment],Vector=Metabolites[y],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[z]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Precup2012 - Mathematical modeling of cell dynamics after allogeneic bone marrow transplantation,Vector=Compartments[compartment],Vector=Metabolites[z],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <ListOfUnitDefinitions>
    <UnitDefinition key="Unit_0" name="meter" symbol="m">
      <Expression>
        m
      </Expression>
    </UnitDefinition>
    <UnitDefinition key="Unit_2" name="second" symbol="s">
      <Expression>
        s
      </Expression>
    </UnitDefinition>
    <UnitDefinition key="Unit_8" name="item" symbol="#">
      <Expression>
        #
      </Expression>
    </UnitDefinition>
    <UnitDefinition key="Unit_17" name="liter" symbol="l">
      <Expression>
        0.001*m^3
      </Expression>
    </UnitDefinition>
    <UnitDefinition key="Unit_34" name="day" symbol="d">
      <Expression>
        86400*s
      </Expression>
    </UnitDefinition>
  </ListOfUnitDefinitions>
</COPASI>
