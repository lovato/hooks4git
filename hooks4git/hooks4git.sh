#!/bin/bash
if [ -x "$(command -v hooks4git)" ]; then
    hooks4git -t $(basename $0)
fi