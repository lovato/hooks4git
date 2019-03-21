#!/bin/bash
docker run --network host -v $(pwd):/tmp/hooks4git:ro -w /tmp/hooks4git -it lovato/bob-python