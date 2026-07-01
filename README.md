# SnapClass

SnapClass is a Streamlit classroom-management app with face and voice attendance, teacher dashboards, student enrollment, leave management, and Supabase persistence.

## Local development

Use Python 3.11 from the repository root:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
.\venv\Scripts\python.exe -m streamlit run app.py
```

Fill `.streamlit/secrets.toml` before starting. Never commit that file.

## Deploy to Streamlit Community Cloud

1. Create a Supabase project.
2. Run `supabase_schema.sql` in **Supabase Dashboard → SQL Editor**. The final statements remove direct anonymous access to private classroom and biometric data.
3. In **Supabase Dashboard → Project Settings → API Keys**, copy the server-side `service_role` key. Treat it as a password; never put it in Git or browser code.
4. Push this repository to GitHub. Do not commit `venv/` or `.streamlit/secrets.toml`.
5. Open <https://share.streamlit.io>, create an app, and select:
   - Repository: this GitHub repository
   - Branch: your deployment branch
   - Main file: `app.py`
   - Python: **3.11** in Advanced settings
6. In **App settings → Secrets**, paste:

```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your-service-role-key"
APP_URL = "https://your-custom-subdomain.streamlit.app"
```

7. Deploy. After choosing the final custom subdomain, update `APP_URL` to that exact HTTPS URL and reboot the app.

## Deployment notes

- Static assets are served from `static/` through `.streamlit/config.toml`.
- `requirements.txt` uses the prebuilt `dlib-bin` package so Community Cloud does not compile dlib from source.
- `packages.txt` installs the small native build/audio libraries used by voice processing.
- Community Cloud installs a fresh environment; the local `venv/` is intentionally excluded.
- Camera access requires HTTPS, which `*.streamlit.app` provides.
- Face and voice embeddings are biometric data. Obtain consent, define retention/deletion rules, and restrict deployment access as required by local law and institutional policy.

## Troubleshooting

Check **Manage app → Logs** first. Typical setup errors are a missing service-role secret, an incorrect `APP_URL`, or selecting a Python version other than 3.11.
