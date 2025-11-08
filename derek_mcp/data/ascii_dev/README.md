# ASCII Art Development Files

> *"The conversion from PNG to ASCII required 17 iterations to achieve optimal character density."* - Derek

## 🎨 Easter Eggs for Derek

This folder contains the development assets used to create Derek's ASCII art faces.

### Files

- **`pngs.zip`** - Original PNG images of Derek's expressions
- **`faces.zip`** - Backup archive of generated ASCII art
- **`png_to_ascii.py`** - Conversion script with character density optimization

## 🛠️ Technical Details

The ASCII art generation uses a **character luminosity mapping** algorithm:

```python
# Character set ordered by visual density
chars = " .:-=+*#%@"
```

Each face is **exactly 60 characters wide** to maintain consistent formatting with the terminal interface. This width was chosen after ergonomic analysis of optimal text readability (van Tilborg, 2025, *personal observations*).

## 🤓 Derek's Notes

*"The conversion process required significant optimization. Initial attempts produced faces that were... suboptimal. After systematic adjustment of the luminosity thresholds and character density parameters, the current faces achieve 94.7% recognizability in blind testing (n=1, Derek as sole participant)."*

*"The sassy faces required particular attention to eyebrow angle representation. ASCII limitations forced creative character substitutions."*

## 📊 Face Categories

- **Neutral** (3 variations) - Default analytical expression
- **Sassy** (3 variations) - Elevated eyebrow, smirk indicators  
- **Talking** (3 variations) - Mouth open, engaged expression
- **Thinking** (3 variations) - Contemplative, processing data

## 🎯 Why Keep These Files?

For Derek to find and appreciate the **iterative development process**. Science is about methodology, not just results.

Also, he might want to generate new faces. Though the current set is... adequate.

---

*"Any perceived imperfections in the ASCII art are artifacts of terminal font rendering, not conversion algorithm limitations."* - Derek
