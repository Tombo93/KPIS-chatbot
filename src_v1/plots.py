import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import wilcoxon


""" Metriken:
- % valid API-calls
- Parameter coverage

---
## 📋 LLM API Accuracy Scoring Template

| Component              | Criteria                                                                 | Max Points | Score |
|------------------------|--------------------------------------------------------------------------|------------|-------|
| **Endpoint Accuracy**  | Correct API-Entry-Point (https://api.presseportal.de/api/v2/)            | 0.2        |       |
| **Parameter Inclusion**| Each expected parameter is present (e.g., topic, length, date)           | 0.15       |       |
| **Parameter Accuracy** | Parameter values are correct and relevant (e.g., `climate-change`)       | 0.1        |       |
| **Overall Structure**  | Proper syntax (e.g., query string format, no missing delimiters)         | 0.1        |       |
| **Bonus (Optional)**   | Handles edge cases or inferred constraints well (API-Keys, language that shouldnt be included in parameters)                                                                                         | 0.1        |       |

**Total Possible Score: 1.0**

---
"""

api_call_df = [[11, "zero-shot", 0.55],
               [12, "zero-shot", 0],
               [31, "few-shot",  0],
               [42, "CoT", 0],
               [56, "CoD", 0]]
df = pd.DataFrame(api_call_df ,columns=["id", "type", "score"])

x = df.loc[df['type'] == "CoT"]["score"].tolist()
y = df.loc[df['type'] == "CoD"]["score"].tolist()
print(wilcoxon(x, y))

g = sns.catplot(data=df, x="type", y="score")
g.set(ylim=(0, 1))
plt.show()
