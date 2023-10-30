Examples
===============

Segmentor
----------

Take a paragraph describing a synthetic procedure, like the following:

::
   synt_example = "3-(4-chloro-2-fluoro-5-hydroxyphenyl)6-trifluoromethyl-2,4(1H,3H)-pyrmidinedione (2.5 g) was added to an ice cooled con. nitric acid (50 ml). After stirring for 1 hr, the reaction mixture was poured into ice-cold water. The yellow crystals were collected by filtration to afford the title compound (0.9 g). The filtrate was extracted by ethyl acetate (200 ml) and washed with brine. The organic phase was dried over anhydrous sodium sulfate. After removal of the solvent, 0.6 g of title compound was obtained as yellow crystal."

To segment this paragraph into multiple semantically distinct steps, use `Segmentor`.

Initialize it by specifying a language model, and an appropriate API key (e.g. OpenAI) if needed.

.. code-block:: python

  gpt4_segment = Segmentor("gpt4")
  segm_paragraph = gpt4_segment.syn2segment(synt_example)

The result should look like this:

.. code-block:: JSON

  {
    {
      "text segment": "3-(4-chloro-2-fluoro-5-hydroxyphenyl)6-trifluoromethyl-2,4(1H,3H)-pyrmidinedione (2.5 g) was added to an ice cooled con. nitric acid (50 ml). After stirring for 1 hr, the reaction mixture was poured into ice-cold water.",
      "text class": "reaction set-up",
      "explanation": "this is the reaction set-up because the main reactant (3-(4-chloro-2-fluoro-5-hydroxyphenyl)6-trifluoromethyl-2,4(1H,3H)-pyrmidinedione) is added to the solvent (con. nitric acid) and the reaction condition (ice cooled, stirring for 1 hr) is specified.",
      "step order": "1"
    },
    {
      "text segment": "The yellow crystals were collected by filtration to afford the title compound (0.9 g).",
      "text class": "work-up",
      "explanation": "this is the work-up step because the product is isolated from the reaction mixture by filtration.",
      "step order": "2"
    },
    {
      "text segment": "The filtrate was extracted by ethyl acetate (200 ml) and washed with brine. The organic phase was dried over anhydrous sodium sulfate. After removal of the solvent, 0.6 g of title compound was obtained as yellow crystal.",
      "text class": "work-up",
      "explanation": "this is the work-up step because the filtrate is extracted, washed, dried, and the solvent is removed to obtain the product.",
      "step order": "3"
    }
  }


