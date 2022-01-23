#!/usr/bin/env bash

function basic(){
  rm -rf $1 || true
  mkdir -p $1
  cd $1

  git init

  mkdir src
  touch src/file{1,2,3}.txt
  git add src/file1.txt src/file2.txt src/file3.txt
  git commit -m 'Initial'

  touch src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 added'

  git checkout -b 'branch1'
  echo "modification 1" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 modified'

  echo "modification 2" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 revised'

  git checkout -b 'branch2'
  echo "modification 2" >> src/file1.txt
  git add src/file1.txt
  git commit -m 'File 1 modified'

  echo "modification 2.2" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 revised 2'

  echo "modification 2.3" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 revised 3'

  echo "modification 2.4" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 revised 4'

  echo "modification 2.4.1" >> src/file3.txt
  git add src/file3.txt
  git commit -m 'File 3 revised 2'

  echo "modification 2.5.1" >> src/file1.txt
  git add src/file1.txt
  echo "modification 2.5.2" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 1 revised2, File 4 revised 5'

  echo "modification 2.6" >> src/file4.txt
  git add src/file4.txt
  git commit -m 'File 4 revised 6'

  echo "modification 2.7" >> src/file4.txt
  echo "modification 2.8" >> src/file1.txt
  git add src/file4.txt
  git add src/file1.txt

  git status
  git log --oneline

}

set -e
$1 tmp/$2
