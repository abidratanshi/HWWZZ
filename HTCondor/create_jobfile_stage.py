import os

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f"chmod -R +x {directory}")

def create_condor_config(nCPUs: int,
                         memory: int,
                         output_dir: str):
    '''
    Creates contents of condor configuration file.
    '''
    cfg = 'Universe          = docker\n'

    cfg += 'docker_image     = cverstege/alma9-gridjob\n'

    cfg += 'accounting_group = cms.higgs \n'

    cfg += 'output_dir       = '+output_dir+'\n'

    cfg += 'executable       = $(filename)\n'

    cfg += 'log              = $(output_dir)log/condor_$(ClusterId).$(ProcId).log\n'

    cfg += 'output           = $(output_dir)out/condor_$(ClusterId).$(ProcId).out\n'

    cfg += 'error            = $(output_dir)err/condor_$(ClusterId).$(ProcId).err\n'

    cfg += 'max_retries      = 3\n'

    cfg += '+JobFlavour      = "longlunch"\n'

    cfg += 'request_memory   = '+str(memory)+' MB\n'

    cfg += 'request_cpus     = '+str(nCPUs)+'\n'

    cfg += 'requirements     = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'

    cfg += 'should_transfer_files   = IF_NEEDED\n'

    cfg += 'when_to_transfer_output  = ON_EXIT\n'

    cfg += 'queue filename matching files'

    for process in processList:
        with open(output_dir + process + '/job_submit.cfg', 'w') as sub:
            sub.write(cfg)
            for file in os.listdir(output_dir + process):
                filename = os.fsdecode(file)
                if filename.endswith('.sh'):
                    sub.write(f' ' + output_dir + process + '/' + filename)

# _____________________________________________________________________________
def create_subjob_script(local_dir: str,
                         source_dir: str,
                         input_dir: str,
                         output_dir: str,
                         output_ana: str,
                         ananame: str):
    '''
    Creates sub-job script to be run.
    '''

    make_dir_if_not_exists(output_dir)
    make_dir_if_not_exists(output_dir+"out")
    make_dir_if_not_exists(output_dir+"log")
    make_dir_if_not_exists(output_dir+"err")

    for process in processList:
        j = 0
        for file in os.listdir(input_dir+process):
            make_dir_if_not_exists(output_dir+process)
            g = input_dir + process + '/' + file + ' '
            scr  = '#!/bin/bash\n\n'
            scr += 'source ' + source_dir + 'setup.sh\n\n'
            scr += 'cd ' + local_dir + '\n\n'
            scr += 'fccanalysis run ' + ananame + ' --batch '
            scr += f' --output  ' + output_ana + process + '/' + 'chunk_'+str(j)+'.root --files-list  ' + g
            scr += '\n\n'
            with open(output_dir + process + '/submit_chunk_' + str(j) + '.sh', 'w') as sh:
                sh.write(scr)
            j+=1
            #print(f"SUBMISSION FIlE CREATED: {process}, chunk {j-1}")

def submit_jobs(output_dir: str):
    for process in processList:
        dir = output_dir + process
        num_files = len(os.listdir(dir))-1
        os.system(f"chmod -R +x {dir}")
        os.system(f"condor_submit {dir}/job_submit.cfg")
        print(f"GOOD SUBMISSION: {process} with {num_files} chunks")

processList = {

    # Signal
    'wzp6_ee_eeH_HWW_ecm365':   {},
    'wzp6_ee_mumuH_HWW_ecm365': {},
    'wzp6_ee_eeH_HZZ_ecm365':   {},
    'wzp6_ee_mumuH_HZZ_ecm365': {},

    # Background
    'p8_ee_WW_ecm365': {},
    'p8_ee_ZZ_ecm365': {},
    'p8_ee_tt_ecm365': {},
}

inputDir = "/ceph/sgiappic/HiggsCP/winter23/"
output = '/work/sgiappic/HTCondor/stage1_test/' ##output directory of submission files, needs to be different to have unique submission files
outputDir = '/ceph/sgiappic/HiggsCP/stage1_ecm240_test/' ##output directory of stage2 samples
localDir = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/'
sourceDir = '/ceph/sgiappic/FCCAnalyses/'
Filename = 'analysis_stage1.py'

nCPUS = 1
Memory = 10000

create_subjob_script(localDir, sourceDir, inputDir, output, outputDir, Filename)

create_condor_config(nCPUS, Memory, output)

submit_jobs(output)
