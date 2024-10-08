#!/bin/bash

# Security hardening consist of 5 compile and link time options
# specified below:
USE_STACK_PROTECTOR=1
USE_FORTIFY_SOURCE=1
USE_PIE=1
USE_ZRELRO=1
USE_ZNOW=1

echo "Using options: $@"

SPECFILE="$(dirname $(gcc --print-libgcc-file-name))/../specs"

# Enable/disable triggers
case $1 in
none)
  rm -f $SPECFILE
  exit 0
  ;;
nofortify)
  USE_FORTIFY_SOURCE=0
  ;;
nopie)
  USE_PIE=0
  ;;
nonow)
  USE_ZNOW=0
  ;;
*)
  ;;
esac

# Populate gcc spec variables in according to enabled triggers
CC1_EXTRA=""
CC1PLUS_EXTRA=""
CPP_EXTRA=""
LIBGCC_EXTRA=""
LINK_EXTRA=""

if [ $USE_STACK_PROTECTOR -eq 1 ]; then
  CC1_EXTRA="$CC1_EXTRA %{!fno-stack-protector-strong:-fstack-protector-strong}"
  CC1PLUS_EXTRA="$CC1PLUS_EXTRA %{!fno-stack-protector-strong:-fstack-protector-strong}"
fi

if [ $USE_FORTIFY_SOURCE -eq 1 ]; then
  CPP_EXTRA="$CPP_EXTRA %{O1|O2|O3|Os|Ofast:-D_FORTIFY_SOURCE=2}"
fi

if [ $USE_PIE -eq 1 ]; then
  CC1_EXTRA="$CC1_EXTRA %{fno-pie|fno-PIE|fpic|fPIC|fPIE|shared:;:-fpie}"
  CC1PLUS_EXTRA="$CC1PLUS_EXTRA %{fno-pie|fno-PIE|fpic|fPIC|fPIE|shared:;:-fpie}"
  # pie flag requires shared libgcc_s during linking.
  LIBGCC_EXTRA="$LIBGCC_EXTRA %{!static:--as-needed -lgcc_s --no-as-needed}"
  LINK_EXTRA="$LINK_EXTRA %{r|nostdlib|fno-pie|fno-PIE|fno-pic|fno-PIC|shared|static:;:-pie}"
fi

if [ $USE_ZRELRO -eq 1 ]; then
  LINK_EXTRA="$LINK_EXTRA %{!norelro:-z relro}"
fi

if [ $USE_ZNOW -eq 1 ]; then
  LINK_EXTRA="$LINK_EXTRA %{!nonow:-z now}"
fi

# Create gcc spec file
echo "# Security hardening flags" > $SPECFILE
if [ -n "$CC1_EXTRA" ]; then
  echo -en "\n
*cc1:
+$CC1_EXTRA" >> $SPECFILE
fi

if [ -n "$CC1PLUS_EXTRA" ]; then
  echo -en "\n
*cc1plus:
+$CC1PLUS_EXTRA" >> $SPECFILE
fi

if [ -n "$CPP_EXTRA" ]; then
  echo -en "\n
*cpp:
+$CPP_EXTRA" >> $SPECFILE
fi

if [ -n "$LIBGCC_EXTRA" ]; then
  echo -en "\n
*libgcc:
+$LIBGCC_EXTRA" >> $SPECFILE
fi

if [ -n "$LINK_EXTRA" ]; then
  echo -en "\n
*link:
+$LINK_EXTRA" >> $SPECFILE
fi
