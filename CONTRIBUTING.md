# Contributing to Nuclio Templates

## Values file

The values file consists of a collection of "field descriptors" to be rendered in Nuclio UI in the "Template parameters" dialog.

The root of the file is a dictionary.   
For each parameter defined in the template YAML, i.e. `{{ .ParamName }}`, there should be a key in the root dictionary, i.e. `ParamName`.  

For example, for the following template:
```yaml
metadata:
  name: my-function-template
spec:
  minReplicas: {{ .ParamName1 }}
  maxReplicas: {{ .ParamName2 }}
```
the values should look like:
```yaml
ParamName1:
    # field descriptor for paramName1
ParamName2:
    # field descriptor for paramName2
```

**Note:** having duplicate keys in the dictionary implies invalid YAML, but nevertheless if somehow the Nuclio UI receives such duplicates it will consider the first one only and skip the rest.

### Field descriptor

The field descriptor is a dictionary that consists of:
- [Common properties](#common-properties): in the root of the dictionary.
- [Kind-specific properties](#kind-specific-properties): grouped together and nested in `attributes` key in the root of the field descriptor.

So the basic structure is as follows:
```yaml
SomeParamName:
  commonProperty1: value1
  commonProperty2: value2
  attribtues:
    kindSpecificProperty1: value3
    kindSpecificProperty2: value4
```

#### Common properties

|Property|Type|Required?|Defaults to|Description|
| :--- | :--- | :--- | :--- | :--- |
|`kind`|string|Yes|-|The type of UI component to render. See [table](#kinds) below with available values.|
|`displayName`|string|Yes|-|The label of the field.|
|`description`|string|No|`''`|Concise explanation to the user on the meaning of this field, how to use it, its effects, etc.<br/>In case it is provided and not empty, a question mark icon will be displayed to the right of the field's label and on hovering it a tooltip will be displayed with this property's value.|
|`required`|boolean|No|`false`|Set to `true` to prevent the form from submitting while this field is empty.|
|`order`|number|No|-|Determine the order by which the fields should be listed. All fields that has no or empty `order` will be displayed together in some indeterminate order _after_ the rest of the (ordered) fields.|

All other properties at root level will be ignored.

#### Kinds

|Kind|UI component|
| :--- | :--- |
|[`'string'`](#string)|single-line text-box|
|[`'number'`](#number)|number input box (with increment/decrement arrows)|
|[`'choice'`](#choice)|drop-down menu (choose one of many)|

#### Kind-specific properties

The set of properties nested in `attributes` is determined by the `kind` value.  
Below are lists of the relevant properties to each of the different kinds of fields.  
All other properties nested in `attribtues` will be ignored.

##### string

|Property|Type|Required?|Defaults to|Description|
| :--- | :--- | :--- | :--- | :--- |
|`defaultValue`|string|No|`''`|The initial value.|
|`maxLength`|number|No|-|The maximum number of characters to allow.|
|`password`|boolean|No|`false`|Set to `true` to obscure the entered characters.|

Example:

```yaml
Table:
  displayName: Table name
  kind: string
  description: "Name of target table"
  required: true
  attributes:
    defaultValue: table
    maxLength: 128
```

![image](https://user-images.githubusercontent.com/13918850/50565121-3cbd2500-0d34-11e9-9798-21879d5b8e1f.png)

##### number

|Property|Type|Required?|Defaults to|Description|
| :--- | :--- | :--- | :--- | :--- |
|`defaultValue`|number|No|`''`|The initial value.|
|`minValue`|number|No|-|The minimal valid value.|
|`maxValue`|number|No|-|The maximum valid value.|
|`step`|number|No|1|The number to add to/subtract from the current value when clicking on the up/down arrows, respectively.|
|`allowNegative`|boolean|No|`false`|Set to `true` to allow entering negative values. If not `true` and `minValue` is set to a negative value, then `minValue` will automatically be set to 0 instead.

Example:

```yaml
IgzV3fPort:
  displayName: v3io-frames port
  kind: number
  description: "v3io-frames endpoint port"
  required: true
  attributes:
    defaultValue: 8081
    minValue: 5000
    maxValue: 99999
```

![image](https://user-images.githubusercontent.com/13918850/50565111-26af6480-0d34-11e9-9ff0-2bbebb8d5d18.png)

##### choice

|Property|Type|Required?|Defaults to|Description|
| :--- | :--- | :--- | :--- | :--- |
|`choices`|list of strings|Yes|-|The options in the drop-down menu.|
|`defaultValue`|string|No|`''`|The initial value of the field. Should match one of the strings in `choices` list. If not, a "Please select…" placeholder will be displayed.|


Example:

```yaml
TargetLang:
  displayName: Target language
  kind: choice
  description: "Target language for translation (e.g. he, fr)"
  required: true
  attributes:
    choices: [fr, he, es, it, ru]
    defaultValue: fr
```

![image](https://user-images.githubusercontent.com/13918850/50565098-04b5e200-0d34-11e9-91d1-acdd7f5eada3.png)
