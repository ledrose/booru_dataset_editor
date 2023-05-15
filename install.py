import launch

if not launch.is_installed("PyPAC"):
    launch.run_pip("install PyPAC==0.16.4", 'requirements for BooruDatasetEditor')