import google.generativeai as genai
print([name for name in dir(genai) if not name.startswith('_')])
print('has generate', hasattr(genai, 'generate'))
print('has text', hasattr(genai, 'text'))
print('has predict', hasattr(genai, 'predict'))
print('has Completion', hasattr(genai, 'Completion'))
print('has responses', hasattr(genai, 'responses'))
