"""Host-compatible LibreOffice fallback; bundled LO requires unavailable glibc 2.38."""
import importlib.util
spec=importlib.util.spec_from_file_location('renderer','/home/panu/.codex/plugins/cache/openai-primary-runtime/documents/26.1011.11113/skills/documents/render_docx.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module._resolve_soffice=lambda:'/usr/bin/soffice'
module.main()
