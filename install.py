import launch

if not launch.is_installed("pypac"):
    launch.run_pip("install pypac==0.16.4", 'requirements for BooruDatasetEditor')