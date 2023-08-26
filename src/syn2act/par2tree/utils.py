"""prompts. rename"""

from langchain import PromptTemplate, chains

from syn2act.segment.gpt import llm_gpt4

tree_extract_prompt = """Your goal is to extract structured information from the user's input about how compounds are related in a chemical synthesis. When extracting information, please make sure it matches the type of information exactly. Do not add any attributes that do not appear in the schema shown below.

```
{ // Information about a compound produced in a chemical reaction, also called product
  reference_num: string // Number code used to reference the compound
  compound_name: string // Name of the compound
  reagents: [ // List of reagents from which the compound was synthesized.
    {
          reference_num
          compound_name
          reagents
     },
    ]
}

The reagents list in the schema should contain other compound objects. If the user's input does not specify how a reagent was made from other compounds, the reagents list should remain empty. If the compound has no reference_num, copy the compound's name to this field. If there are multiple products included in the user's input, create a separate schema for each and output them as a list
[{ first compound }, { second compound },]
    
Please output the extracted information in JSON format. Do not output anything except for the extracted information. Do not add any clarifying information. Do not add any fields that are not in the schema. If the text contains attributes that do not appear in the schema, please ignore them. 
    
To produce the output, think step-by-step, but do not include any of your reasoning in the output.
 
{{ examples }}

Input: {{ user_input }}
Output: """


examples = """
Input: {'products': [{'name': '(2-{(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-4-methyl-3-methylidenetetrahydro-2H-pyran-2-yl}ethoxy)-(tert-butyl)diphenylsilane',
   'reference_num': '19a',
   'mass': '734 mg',
   'yield': '92%'}],
 'steps': [{'type': 'set-up',
   'text': '(2-{(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-4-methyl-3-methylidenetetrahydro-2H-pyran-2-yl}ethoxy)-(tert-butyl)diphenylsilane (19a): To a stirred solution of methyl triphenyl phosphonium bromide (2.62 g, 7.34 mmol, 5.0 equiv) in THF (40 mL) at −78 °C was added dropwise n-butyl lithium (1.6 M in hexanes, 4.13 mL, 6.62 mmol, 4.5 equiv), and the reaction mixture was warmed to 0 °C. After 0.5 h, a solution of ketone 20a (800 mg, 1.47 mmol, 1.0 equiv) in THF (15 mL) was added to the preformed ylide solution and the resulting mixture was allowed to warm to 23 °C. After 1 h, the reaction mixture was carefully quenched by the addition of saturated aqueous NH4Cl solution (80 mL). The aqueous layer was extracted with EtOAc (3 × 30 mL) and the combined organic layers were dried over anhydrous Na2SO4, ﬁltered, and concentrated under reduced pressure.'}]}
   
Output: 
{
    "reference_num": "19a",
    "compound_name": "(2-{(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-4-methyl-3-methylidenetetrahydro-2H-pyran-2-yl}ethoxy)-(tert-butyl)diphenylsilane",
    "reagents": [
      {
          "reference_num": "methyl triphenyl phosphonium bromide",
          "compound_name": "methyl triphenyl phosphonium bromide",
          "reagents": []
      },
      {
          "reference_num": "n-butyl lithium",
          "compound_name": "n-butyl lithium",
          "reagents": []
      },
      {
          "reference_num": "20a",
          "compound_name": "ketone",
          "reagents": []
      }
    ]
  }

Input: {'products': [{'name': '2-{(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-4-methyl-3-methylidenetetrahydro-2H-pyran-2-yl}ethanol', 'reference_num': 'S1', 'mass': '264 mg', 'yield': '94%'}], 'steps': [{'type': 'set-up', 'text': '2-{(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-4-methyl-3-methylidenetetrahydro-2H-pyran-2-yl}ethanol (S1): To a stirred solution of oleﬁn derivative 19a (500 mg, 0.921 mmol, 1.0 equiv) in THF (20 mL) at 0 °C was added dropwise tetra-n-butylammonium ﬂuoride (1 M in THF, 0.920 mL, 0.920 mmol, 1.0 equiv), and the reaction mixture was allowed to warm to 23 °C. After 2.5 h, the reaction mixture was quenched by the addition of saturated aqueous NH4Cl solution (15 mL). The aqueous layer was extracted with EtOAc (3 × 15 mL) and the combined organic layers were dried over anhydrous Na2SO4, ﬁltered, and concentrated under reduced pressure.'}]}

Output:
{
    "reference_num": "S1",
    "compound_name": "2-{(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-4-methyl-3-methylidenetetrahydro-2H-pyran-2-yl}ethanol",
    "children": [
      {
          "reference_num": "19a",
          "compound_name": "oleﬁn derivative",
          "children": []
      },
      {
          "reference_num": "tetra-n-butylammonium ﬂuoride",
          "compound_name": "tetra-n-butylammonium ﬂuoride",
          "children": []
      }
    ]
  }
"""


tree_extract_template = PromptTemplate.from_template(
    template=tree_extract_prompt, template_format="jinja2"
)
tree_chain = chains.LLMChain(prompt=tree_extract_template, llm=llm_gpt4)
