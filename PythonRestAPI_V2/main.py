    for deployment in deployments.items:
        print("Name\tREADY")
        print(f"{deployment.metadata.name}\t{deployment.status.ready_replicas}/{deployment.status.replicas}")