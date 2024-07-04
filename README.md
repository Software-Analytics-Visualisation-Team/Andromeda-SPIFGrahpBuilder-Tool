# SPIF-to-SVIF-Tool

## Set up:
1. Setup a local Galaxy instance.
2. Go to the directory `galaxy/tools/moonshot/` and clone this repository. (Create the moonshot directory if it doesn't exist yet)
3. Change the galaxy tool configuration at `galaxy/config/tool_conf.xml.sample` by adding:
   ```
   <section name="Moonshot" id="moonshot">
     <tool file="moonshot/SPIF-to-SVIF-Tool/owl_to_json.xml"/>
   </section>
   ```
   
## How to use the tool:
1. Build and run Galaxy as normal.
2. Navigate on the left `Tools column > Moonshot > SPIF-to-SVIF-Tool`.
3. Upload and select a SPIF file.
4. Click on "Run Tool" button.


![](https://github.com/rsatrioadi/phd/raw/main/figures/compacted.svg)

#### Edge definitions:
- S holds T when Structure S has a variable of Type T.
- S accepts T when Structure S has an operation that has a parameter of Type T.
- S returns T when Structure S has an operation with return Type T.
- S constructs T when Structure S has a script that instantiates Structure T.
- S calls T when Structure S has a script that calls an operation of Structure T. It is what is usually considered in a “dependency graph”.
- S accesses T when Structure S has a script that directly access a field of Structure T.

For more information about the format see the section "LPG schema for abstract structure knowledge" [here](https://github.com/rsatrioadi/phd/blob/main/representation.md).

## How to run unit tests
Run the command: 
```
python -m unittest discover -s tests
```
Add `-v` flag at the end for more detailed testing <br/>
Depending on how your python environment is set up the command can also be:
```
python3 -m unittest discover -s tests
```

## Implementation progress:
### Nodes:
- [x] Primitive
- [x] Container
- [x] Structure

### Edges:
- [x] contains (container contains structure)
- [x] contains (container contains container)
- [x] contains (structure contains structure)
- [x] holds
- [x] returns
- [x] accepts
- [x] accesses
- [x] calls
- [x] constructs
- [x] extends
- [x] implements

### Structure node properties:
The unimplemented ones left are not visualized using ClassViz.

- [x] kind
- [x] isPublic
- [x] isClass
- [x] isInterface
- [x] isAbstract
- [x] isEnum
- [x] isStatic
- [ ] sourceText
- [ ] isSerializable
- [ ] isCollection
- [ ] isMap
- [ ] isAWTComponent
- [ ] namedController
- [ ] namedManager
- [ ] namedListener
- [ ] namedTest
- [ ] numFields
- [ ] numPublicFields
- [ ] numPrivateFields
- [ ] numPrimitiveFields
- [ ] numCollectionFields
- [ ] numIterableFields
- [ ] numMapFields
- [ ] numAWTComponentFields
- [ ] ratioPublicFields
- [ ] ratioPrivateFields
- [ ] numMethods
- [ ] numPublicMethods
- [ ] numPrivateMethods
- [ ] numAbstractMethods
- [ ] numGetters
- [ ] numSetters
- [ ] ratioPublicMethods
- [ ] ratioPrivateMethods
- [ ] ratioAbstractMethods
- [ ] ratioGetters
- [ ] ratioSetters
- [ ] ratioGettersToFields
- [ ] ratioSettersToFields
- [ ] numStatementsInMethods
- [ ] averageStatementsPerMethod
- [ ] numParametersInMethods
- [ ] averageParametersPerMethod
- [ ] numBranchingInMethods
- [ ] averageBranchingPerMethod
- [ ] numLoopsInMethods
- [ ] averageLoopsPerMethod
- [ ] accessesIO
- [ ] maxLoopDepth


