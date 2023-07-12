# I am python, not json
{
    # Mode of the task, two option [ray|standalone].
    "run_mode" : "ray",
    # The global seed of pytorch.
    "seed": 42,
    # The global threads num of pytorch.
    "torch_thread_num": 28,
    # Config of accelerator, all items will be transfered to accelerate.Accelerator().
    "accelerator": {
        "gradient_accumulation_steps": 1,
    },
    "datasets": {
        # The type of dataset, now only HuggingfaceDataset is supported.
        "type": "HuggingfaceDataset",
        # The name/path of dataset in huggingface.
        "name": "tatsu-lab/alpaca",
        # Whether to use the datasets.load_from_disk() interface to load data. 
        "load_from_disk": False,
        # Config of dataset, all items will be transfered to datasets.load_dataset() or datasets.load_from_disk().
        "load_config" : {}
    },
    "tokenizer": {
        # The type of dataset, now only HuggingfaceTokenizer is supported.
        "type": "HuggingFaceTokenizer",
        # The name/path of tokenizer in huggingface.
        "name": "EleutherAI/gpt-j-6B",
        # Config of tokenizer, all items will be transfered to transformers.AutoTokenizer.from_pretrained().
        "config": {}
    },
    "model": {
        # The type of model, now only HuggingfaceModelForCausalLM is supported.
        "type": "HuggingFaceModelForCausalLM",
        # The name/path of model in huggingface.
        "name": "EleutherAI/gpt-j-6B",
        # Config of model, all items will be transfered to AutoModelForCausalLM.from_pretrained().
        "config": {
            "trust_remote_code": True
        }
    },
    "optimizer": {
        # The type of optimizer, only DefaultOptimizer is supported. All parameters in model will be optimized by DefaultOptimizer.
        "type": "DefaultOptimizer",
        # The name of optimizer, all optimizers in torch.optim are supported.
        "name": "AdamW",
        # Config of optimizer, all items will be transfered to torch.optim.[name]()
        "config": {
            "lr" : 1e-5,
        }
    },
    "trainer": {
        # The type of trainer, now only DefaultTrainer is supported.
        "type": "DefaultTrainer",
        # Number of train epochs
        "num_train_epochs": 2,
        # The max training step of each epoch, if set to None means unlimited.
        # In most cases this item is for debugging.
        "max_train_step": None,
        # The max evaluating step of each epoch, if set to None means unlimited.
        # In most cases this item is for debugging.
        "max_eval_step": None,
        # Output directory. Only absolute path is supported.
        "output": "/tmp/output",
        "dataprocesser": {
            # The type of dataprocesser. 
            "type": "GeneralProcesser",
            # Number of preprocessing workers.
            "preprocessing_num_workers": 4,
            # Whether to apply batch processing.
            "batched": True,
            # Batch size of batch data processing.
            "batch_size": 1000,
            # train batch size per device
            "per_device_train_batch_size": 2,
            # eval batch size per device
            "per_device_eval_batch_size": 4,
            # Whether the training dataset is shuffle
            "shuffle": True
        },
        "lr_scheduler": {
            # Whether to enable learning rate scheduler
            "enable": True,
            # The max training step of lr_scheduler. This item will be transfered to transformers.get_scheduler().
            "max_train_steps": None,
            # The type of lr_scheduler. This item will be transfered to transformers.get_scheduler().
            "lr_scheduler_type": "linear",
            # Number of warmup steps. This item will be transfered to transformers.get_scheduler().
            "num_warmup_steps": 0,
        },
        "checkpoint": {
            # The root path of checkpoint. Only absolute path is supported
            "root_path": "/tmp/checkpoint",
            # The model name of this task.
            "model_name": "test"
        }
    },
    # Ray related configuration, Only used when mode is set to ray
    "ray_config": {
        # The config of ray.init. All items will be tranfered to ray.init().
        # More information can refer to https://docs.ray.io/en/latest/ray-core/api/doc/ray.init.html
        "init": {
            # Environment variables for ray workers
            "runtime_env": {
                "env_vars": {
                    "OMP_NUM_THREADS": "28", 
                    "ACCELERATE_USE_CPU": "True", 
                    "ACCELERATE_MIXED_PRECISION": "no",
                    "CCL_WORKER_COUNT": "2",        # CCL setting
                    "CCL_LOG_LEVEL": "info",
                    "WORLD_SIZE": "2",    # Enable multi-process
                }
            },
            # The address of the Ray cluster to connect to.
            "address": "auto",
            # The IP address of the node that we are on.
            "_node_ip_address": "127.0.0.1",
        },
        "scaling_config": {
            # Number of worker.
            "num_workers": 2,
            # The amount of resources per worker.
            "resources_per_worker": {
                "CPU": 28
            },
            # The placement strategy to use for the placement group of the Ray actors.
            "placement_strategy": "SPREAD"
        },
        "torch_config": {
            # The backend of the communication library.
            "backend" : "ccl",
        },
        "failure_config": {
            # The maximum number of restarts when task fail.
            "max_failures": 5
        },
        "run_config": {
            # Local dir to save training results to.
            "local_dir": "/tmp/llm-ray"
        }
    }
}