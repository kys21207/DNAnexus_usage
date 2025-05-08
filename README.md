# DNAnexus_usage
### 1. Download bcftools and plink2
bcftools <br>
git clone --recurse-submodules https://github.com/samtools/htslib.git <br>
git clone https://github.com/samtools/bcftools.git <br>
cd bcftools <br>
The following is optional: <br>
   autoheader && autoconf && ./configure --enable-libgsl --enable-perl-filters <br>
make <br>

plink2 <br>
wget https://s3.amazonaws.com/plink2-assets/alpha6/plink2_linux_x86_64_20241222.zip <br>
unzip plink2_linux_x86_64_20241222.zip <br>

MAGMA <br>
mkdir MAGMA <br>
cd MAGMA <br>
wget https://vu.data.surfsara.nl/index.php/s/zkKbNeNOZAhFXZB/download <br>
mv download magma_v1.10.zip <br>
unzip magma_v1.10.zip <br>

### 2. conda 
For example gwaslab <br>
conda env create -n gwaslab_test -c conda-forge python=3.9 <br>
conda activate gwaslab <br>
pip install gwaslab <br>
For example r-packages <br>
conda create -n env <br>
conda activate env <br>
conda install r-R.utils r-susieR <br>

### 3. docker
Create a docker image or get a docker image created by an app <br>
And <br>
> docker run -it -v $(pwd):$(pwd) -w $(pwd) ghcr.io/neurogenomics/magma.celltyping:latest /bin/bash <br>
> docker run --rm predixcan python /app/PrediXcan.py --help <br>
> docker image is (find the docker image) <br>
