# Glass Compositional Analysis Project

A data science project for analyzing ancient glass composition using archaeological datasets, with integrated AI assistance for interpretation and insights.

## Dataset

This project uses data from:

**Phelps, M., Freestone, I. C., Gorin-Rosen, Y., & Gratuze, B. (2016)**  
*"Natron glass production and supply in the late antique and early medieval Near East: The effect of the Byzantine-Islamic transition."*  
Journal of Archaeological Science, 75, 57-71.  
DOI: [10.1016/j.jas.2016.06.016](https://www.sciencedirect.com/science/article/pii/S0305440316301169)

### Dataset Description
- **128 glass samples** from the late antique and early medieval Near East
- **6 composition groups**: N-1 (54), N-3 (50), N-2 (17), N-3 (Co) (3), N-4 (2), N-3 (Mn) (2)
- **Chemical composition data** for major oxides (SiO₂, Na₂O, CaO, Al₂O₃, K₂O, MgO, FeO, TiO₂, P₂O₅)
- **Focus on natron glass production** and supply chains during the Byzantine-Islamic transition
- **Metadata** including sample IDs, site information, chronology, and visual characteristics

## Project Features

- **Data Cleaning Pipeline**: Standardizes data format and handles missing values
- **AI Integration**: Ollama-powered analysis interpretation and research assistance
- **Web Interface**: Open WebUI for natural language interactions with AI
- **Reproducible Environment**: Docker-based setup for consistent results

## Future addition
- **Compositional Analysis**: Bivariate analysis using oxide ratios (CaO/Al₂O₃ vs Na₂O/SiO₂)
- **Statistical Analysis**: Group comparison and significance testing


## Quick Start

### Prerequisites
- Docker Desktop
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd glass-analysis-project
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Start Docker services**
   ```bash
   docker compose up -d
   ```

4. **Access the interfaces**
   - Jupyter Lab: http://localhost:8888
   - Open WebUI (AI Chat): http://localhost:3001
   - Ollama API: http://localhost:11435

### Usage

1. **Data Cleaning**
   - Run `notebooks/01_data_cleaning.ipynb` to clean and standardize the dataset
   - This generates cleaned files in `data/processed/`

2. **Future Analysis** (planned)
   - Data exploration and visualization
   - Compositional analysis with oxide ratios
   - Statistical group comparisons

3. **AI Assistance**
   - Use Open WebUI to ask questions about your cleaning results
   - Get interpretation help and next steps advice

## Project Structure

```
glass-analysis-project/
├── data/
│   ├── raw/                 # Original dataset (phelps_et_al_2016.xlsx)
│   ├── processed/           # Cleaned data (generated after cleaning)
│   └── external/            # Additional data sources
├── notebooks/
│   └── 01_data_cleaning.ipynb  # Data cleaning and standardization
├── src/
│   └── ollama_helper.py     # AI integration utilities
├── results/
│   ├── figures/             # Generated plots (future)
│   └── reports/             # Analysis reports (future)
├── docker-compose.yml       # Service orchestration
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md
```

## Analysis Workflow

### 1. Data Preparation
```python
import pandas as pd
df = pd.read_excel('data/processed/phelps_2016_cleaned.xlsx')
```

### 3. AI-Assisted Interpretation
```python
from src.ollama_helper import setup_ollama

ai = setup_ollama("llama2")
interpretation = ai.ask("What do these oxide ratio patterns suggest about ancient glass production?")
```

## Key Research Questions

to be added...

## Dependencies

### Python Packages
- pandas >= 2.1.4
- numpy >= 1.24.3
- matplotlib >= 3.7.2
- seaborn >= 0.12.2
- scikit-learn >= 1.3.0
- scipy >= 1.11.3
- openpyxl >= 3.1.2

### Docker Services
- **Jupyter Lab**: Interactive data analysis environment
- **Ollama**: Local AI model hosting
- **Open WebUI**: Web-based AI chat interface

## Troubleshooting

### Common Issues

**Docker containers won't start:**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Port conflicts:**
- Jupyter: Change port 8888 in docker-compose.yml
- Open WebUI: Change port 3001 in docker-compose.yml
- Ollama: Change port 11435 in docker-compose.yml

**AI not responding:**
```bash
docker exec -it glass-ollama-1 ollama pull llama2
```

**Data loading issues:**
- Ensure Excel file is in `data/raw/phelps_et_al_2016.xlsx`
- Check file permissions and path

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature-name`)
5. Create Pull Request

## Citation

If you use this project in your research, please cite:

```bibtex
@article{phelps2016natron,
  title={Natron glass production and supply in the late antique and early medieval Near East: The effect of the Byzantine-Islamic transition},
  author={Phelps, Matthew and Freestone, Ian C and Gorin-Rosen, Yael and Gratuze, Bernard},
  journal={Journal of Archaeological Science},
  volume={75},
  pages={57--71},
  year={2016},
  publisher={Elsevier},
  doi={10.1016/j.jas.2016.06.016}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original dataset: Phelps et al. (2016)
- AI integration: Ollama and Open WebUI communities
- Analysis framework: Scientific Python ecosystem

## Contact

For questions about this analysis framework, please open an issue in the repository.

---

**Note**: This project is for educational and research purposes. The dataset is used under fair use for academic analysis. For commercial applications, please contact the original authors.
