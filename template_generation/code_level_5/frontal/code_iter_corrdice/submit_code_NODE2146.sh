#!/bin/bash -l
if  QID0_1=$(sbatch -p cpu /HPC_work_dir/code_iter_corrdice/queue_NODE2146_0.sh 2>&1); then
    QID0_1_id=$(echo ${QID0_1} | sed -n -e 's/^.*job //p')
    echo "Job submitted successfully with ID $QID0_1_id"
else
    echo "Job submission failed"
    exit 1
fi

if  QID0_2=$(sbatch -p cpu -d $QID0_1_id /HPC_work_dir/code_iter_corrdice/queue_mergeNODE2146_0.sh 2>&1); then
    QID0_2_id=$(echo ${QID0_2} | sed -n -e 's/^.*job //p')
    echo "Job submitted successfully with ID $QID0_2_id"
else
    echo "Job submission failed"
    exit 1
fi

# second registration and second template
if  QID1_1=$(sbatch -p cpu -d $QID0_2_id /HPC_work_dir/code_iter_corrdice/queue_NODE2146_1.sh 2>&1); then
    QID1_1_id=$(echo ${QID1_1} | sed -n -e 's/^.*job //p')
    echo "Job submitted successfully with ID $QID1_1_id"
else
    echo "Job submission failed"
    exit 1
fi

if  QID1_2=$(sbatch -p cpu -d $QID1_1_id /HPC_work_dir/code_iter_corrdice/queue_mergeNODE2146_1.sh 2>&1); then
    QID1_2_id=$(echo ${QID1_2} | sed -n -e 's/^.*job //p')
    echo "Job submitted successfully with ID $QID1_2_id"
else
    echo "Job submission failed"
    exit 1
fi

sleep_time=120 # seconds
# check to see if job is running
status=`squeue -u $USER_NAME | grep $QID1_2_id`
# while $status is not empty
while [ -n "$status" ]
    do
        sleep $sleep_time
        status=`squeue -u $USER_NAME | grep $QID1_2_id`
    done
iter=1
diff=$(tail -n 1 /HPC_work_dir/log/output.array.${QID1_2_id}.0)
echo "diff: ${diff}"
thre=0.005
while [ `echo "$diff > $thre" | bc` -eq 1 ]
    do
    # do registration if the difference map is greater than 0.005
    ((iter++))
    echo "iter: ${iter} start"



    if  QID1_1=$(sbatch -p cpu /HPC_work_dir/code_iter_corrdice/queue_NODE2146_${iter}.sh 2>&1); then
        QID1_1_id=$(echo ${QID1_1} | sed -n -e 's/^.*job //p')
        echo "Job submitted successfully with ID $QID1_1_id"
    else
        echo "Job submission failed"
        exit 1
    fi

    if  QID1_2=$(sbatch -p cpu -d $QID1_1_id /HPC_work_dir/code_iter_corrdice/queue_mergeNODE2146_${iter}.sh 2>&1); then
        QID1_2_id=$(echo ${QID1_2} | sed -n -e 's/^.*job //p')
        echo "Job submitted successfully with ID $QID1_2_id"
    else
        echo "Job submission failed"
        exit 1
    fi

    echo "iter ${iter}: job submitted!"
    # check to see if job is running
    status=`squeue -u $USER_NAME | grep $QID1_2_id`
    # while $status is not empty
    while [ -n "$status" ]
        do
            sleep $sleep_time
            status=`squeue -u $USER_NAME | grep $QID1_2_id`
        done
    # update diff
    sleep $sleep_time
    diff=$(tail -n 1 /HPC_work_dir/log/output.array.${QID1_2_id}.0)
    echo "diff: ${diff}"
    echo "iter: ${iter} done"
    done
echo "iteration finished!"