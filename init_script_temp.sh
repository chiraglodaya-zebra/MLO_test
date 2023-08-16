pip install -U dbfs:/mnt/adf-lib/al2databrickslibs-libs-rw/adf_library/adf_library-1.4.5+gb7983bc-cp38-cp38-linux_x86_64.whl
pip install -U dbfs:/mnt/adf-lib/al2databrickslibs-libs-rw/ai_core_library/ai_core_library-2.1.0+g99f14f1-cp38-cp38-linux_x86_64.whl
# pip install -U /dbfs/mnt/prod-libraries/datamart_library/datamart_library-1.4.0+g93b2c6b-cp38-cp38-linux_x86_64.whl

wget https://aka.ms/downloadazcopy-v10-linux &&
tar -xvf downloadazcopy-v10-linux &&
rm /usr/bin/azcopy &&
cp ./azcopy_linux_amd64_*/azcopy /usr/bin/ &&
rm downloadazcopy-v10-linux

#dbfs:/mnt/adf-lib/al2databrickslibs-libs-rw/adf_library/adf_library-1.4.5+gb7983bc-cp38-cp38-linux_x86_64.whl