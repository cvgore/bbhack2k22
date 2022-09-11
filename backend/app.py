import font_metrics
import translator

tr = translator.Translator()
tr.load_translation_file("../sample.csv")
print(tr.translate_text("test123"))
# ('szukaj', array([[395.01007  ,  12.6606865], [445.07962  ,  14.329674 ], [444.5371   ,  30.60573  ], [394.46756  ,  28.936743 ]], dtype=float32))
ff = font_metrics.FontFitter()
print(ff.fit_text([[395, 12], [445, 14], [444, 30], [394, 28]], tr.translate_text("szukaj"), 'fontname'))