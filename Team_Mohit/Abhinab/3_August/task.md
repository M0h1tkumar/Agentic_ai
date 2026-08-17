# 6. 3 August Tasks

## Clone/install Multica

Use the official repository and current documentation:

``` bash
git clone <OFFICIAL-MULTICA-REPOSITORY>
cd <MULTICA-REPOSITORY>
```

Then follow the current installation instructions.

Verify the installation using the version's supported commands.

## OmniRoute experiment

The experiment should focus on model/provider routing:

``` text
User Task
   |
   v
Router
   |
   +--> Fast/cheap model
   +--> Reasoning model
   +--> Coding model
   +--> Local model
```

Example routing:

  Task                    Preferred model
  ----------------------- -------------------
  Simple classification   Small/cheap model
  Coding                  Coding model
  Complex reasoning       Reasoning model
  Private documents       Local model
  Large batch             Low-cost model
