import random
import sys

# ----------------------------
# Step 1: Get input from user with validation
# ----------------------------

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_user_input():
    try:
        num_jobs = get_positive_int("Enter number of jobs: ")
        num_resources = get_positive_int("Enter number of machines/resources: ")

        machine_capacities = []
        for i in range(num_resources):
            capacity = get_positive_int(f"Enter capacity for machine {i+1}: ")
            machine_capacities.append(capacity)

        job_durations = []
        for i in range(num_jobs):
            t = get_positive_int(f"Enter duration for job {i+1}: ")
            job_durations.append(t)

        precedence_constraints = []
        print("\nEnter precedence constraints (e.g., '1 2' means job 1 must finish before job 2). Type 'done' when finished:")
        while True:
            try:
                line = input().strip()
                if line.lower() == 'done':
                    break
                a, b = map(int, line.split())
                if 1 <= a <= num_jobs and 1 <= b <= num_jobs:
                    precedence_constraints.append((a-1, b-1))
                else:
                    print(f"Invalid job index. Must be between 1 and {num_jobs}.")
            except ValueError:
                print("Invalid input. Please enter two numbers or 'done'.")

        resource_constraints = []
        print("\nEnter resource constraints (e.g., '1 1' means job 1 cannot run on machine 1). Type 'done' when finished:")
        while True:
            try:
                line = input().strip()
                if line.lower() == 'done':
                    break
                j, r = map(int, line.split())
                if 1 <= j <= num_jobs and 1 <= r <= num_resources:
                    resource_constraints.append((j-1, r-1))
                else:
                    print(f"Invalid input. Jobs 1-{num_jobs}, machines 1-{num_resources}.")
            except ValueError:
                print("Invalid input. Please enter two numbers or 'done'.")

        temporal_constraints = {}
        print("\nEnter temporal constraints (e.g., '1 5' means job 1 cannot start before time 5). Type 'done' when finished:")
        while True:
            try:
                line = input().strip()
                if line.lower() == 'done':
                    break
                j, t = map(int, line.split())
                if 1 <= j <= num_jobs and t >= 0:
                    temporal_constraints[j-1] = t
                else:
                    print(f"Invalid input. Job index 1-{num_jobs}, time >= 0.")
            except ValueError:
                print("Invalid input. Please enter two numbers or 'done'.")

        return job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints
    except (EOFError, KeyboardInterrupt):
        print("\nInput terminated. Exiting...")
        sys.exit(0)

# ----------------------------
# Validity Check
# ----------------------------

def is_valid(schedule, job, start, resource, job_durations, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
    end = start + job_durations[job]

    if job in temporal_constraints:
        if start < temporal_constraints[job]:
            return False

    if (job, resource) in resource_constraints:
        return False

    jobs_on_machine = [(s, e) for j, (s, e, r) in schedule.items() if r == resource and j != job]
    overlapping_jobs = sum(1 for s, e in jobs_on_machine if not (end <= s or start >= e))
    if overlapping_jobs >= machine_capacities[resource]:
        return False

    for before, after in precedence_constraints:
        if after == job and before in schedule:
            if start < schedule[before][1]:
                return False
        elif before == job and after in schedule:
            if end > schedule[after][0]:
                return False

    return True

# ----------------------------
# Backtracking Algorithm
# ----------------------------

def backtracking(job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, auto_split, temporal_constraints):
    best_schedule = None
    best_makespan = float('inf')
    
    # Calculate a tighter bound for max_start
    max_start = max(
        sum(job_durations) // (min(machine_capacities) * num_resources) + 1,  # Theoretical minimum
        max([temporal_constraints.get(i, 0) + job_durations[i] for i in range(len(job_durations))] + [0])  # Temporal constraints
    )

    def try_schedule(schedule, remaining):
        nonlocal best_schedule, best_makespan
        if not remaining:
            end_times = [e for _, (s, e, _) in schedule.items()]
            current_makespan = max(end_times) if end_times else float('inf')
            if current_makespan < best_makespan:
                best_makespan = current_makespan
                best_schedule = schedule.copy()
            return

        job = remaining[0]
        new_remaining = remaining[1:]
        
        # Sort resources by current load
        resources = list(range(num_resources)) if not auto_split else sorted(
            range(num_resources), 
            key=lambda r: sum((e - s) for _, (s, e, r2) in schedule.items() if r2 == r)
        )
        
        # Calculate minimum start time
        min_start = max([schedule.get(dep, (0, 0, 0))[1] for dep, after in precedence_constraints if after == job and dep in schedule] + [temporal_constraints.get(job, 0)])
        
        for resource in resources:
            # Find existing jobs on this resource
            resource_jobs = sorted([(s, e) for _, (s, e, r) in schedule.items() if r == resource])
            
            # Try optimal start times
            potential_starts = [min_start]  # Start with earliest possible time
            
            # Add start times after jobs end
            for _, end in resource_jobs:
                if end >= min_start:
                    potential_starts.append(end)
            
            # Try these specific times
            for start in potential_starts:
                if start > max_start:
                    break
                if is_valid(schedule, job, start, resource, job_durations, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
                    schedule[job] = (start, start + job_durations[job], resource)
                    try_schedule(schedule, new_remaining)
                    del schedule[job]

    try_schedule({}, list(range(len(job_durations))))
    return best_schedule, best_makespan

# ----------------------------
# Genetic Algorithm
# ----------------------------

def generate_random_schedule(job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, auto_split, temporal_constraints):
    schedule = {}
    jobs = list(range(len(job_durations)))
    random.shuffle(jobs)
    max_start = sum(job_durations) * 2

    for job in jobs:
        placed = False
        # تحسين التعامل مع القيود الزمنية
        min_start = temporal_constraints.get(job, 0)  # البدء بالقيد الزمني
        if any(after == job for _, after in precedence_constraints):
            min_start = max(min_start, max([schedule.get(dep, (0, 0, 0))[1] for dep, after in precedence_constraints if after == job and dep in schedule] or [0]))
        
        max_start_job = max(min_start + 1, min(max_start, min_start + sum(job_durations)))
        
        resources = list(range(num_resources)) if not auto_split else sorted(
            range(num_resources), 
            key=lambda r: sum((e - s) for _, (s, e, r2) in schedule.items() if r2 == r)
        )
        
        for _ in range(20):
            resource = random.choice(resources)
            # محاولة البدء بالوقت المحدد في القيد الزمني أولاً
            start = min_start
            if is_valid(schedule, job, start, resource, job_durations, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
                schedule[job] = (start, start + job_durations[job], resource)
                placed = True
                break
                
        if not placed:
            return None
    return schedule

def fitness(schedule):
    if schedule is None:
        return float('inf')
    # Penalize schedules that don't respect temporal constraints
    for job, (start, _, _) in schedule.items():
        if job in temporal_constraints and start < temporal_constraints[job]:
            return float('inf')
    return max(e for _, (s, e, _) in schedule.items())

def crossover(parent1, parent2, job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
    child = {}
    jobs = list(parent1.keys())
    for job in jobs:
        child[job] = parent1[job] if random.random() > 0.5 else parent2.get(job, parent1[job])

    for job, (start, end, resource) in list(child.items()):
        # Ensure temporal constraint is strictly enforced
        min_start = temporal_constraints.get(job, 0)
        if any(after == job for _, after in precedence_constraints):
            min_start = max(min_start, max([child.get(dep, (0, 0, 0))[1] for dep, after in precedence_constraints if after == job and dep in child] or [0]))
            
        if not is_valid({k: v for k, v in child.items() if k != job}, job, start, resource, job_durations, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
            max_start_job = min(sum(job_durations), min_start + job_durations[job] + 5)
            for _ in range(5):
                new_start = min_start  # Always try minimum start time first
                new_resource = random.randint(0, num_resources - 1)
                if is_valid({k: v for k, v in child.items() if k != job}, job, new_start, new_resource, job_durations, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
                    child[job] = (new_start, new_start + job_durations[job], new_resource)
                    break
            else:
                return None
    return child

def mutate(schedule, job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
    job = random.choice(list(schedule.keys()))
    # Ensure temporal constraint is strictly enforced
    min_start = temporal_constraints.get(job, 0)
    if any(after == job for _, after in precedence_constraints):
        min_start = max(min_start, max([schedule.get(dep, (0, 0, 0))[1] for dep, after in precedence_constraints if after == job and dep in schedule] or [0]))
    
    max_start_job = min(sum(job_durations), min_start + job_durations[job] + 5)
    new_start = min_start  # Always try minimum start time first
    new_resource = random.randint(0, num_resources - 1)
    if is_valid(schedule, job, new_start, new_resource, job_durations, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints):
        schedule[job] = (new_start, new_start + job_durations[job], new_resource)
    return schedule

def genetic_algorithm(job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, auto_split, temporal_constraints, population_size=10, generations=20):
    population = []
    while len(population) < population_size:
        s = generate_random_schedule(job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, auto_split, temporal_constraints)
        if s:
            population.append(s)

    best_schedule = None
    best_score = float('inf')

    for _ in range(generations):
        scored = sorted(population, key=fitness)
        if fitness(scored[0]) < best_score:
            best_schedule = scored[0]
            best_score = fitness(best_schedule)

        next_gen = scored[:population_size//2]
        while len(next_gen) < population_size:
            p1, p2 = random.sample(next_gen, 2)
            child = crossover(p1, p2, job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints)
            if child and random.random() < 0.2:
                child = mutate(child, job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints)
            if child:
                next_gen.append(child)
        population = next_gen

    return best_schedule, best_score

# ----------------------------
# Main Program
# ----------------------------

print("\n=== Welcome to the Job Scheduling Solver ===\n")

try:
    algo_choice = input("Choose algorithm (1: Backtracking, 2: Genetic Algorithm): ").strip()
    while algo_choice not in ['1', '2']:
        algo_choice = input("Invalid choice. Please enter 1 or 2: ").strip()

    split_choice = input("Do you want to automatically assign jobs to machines? (yes/no): ").strip().lower()
    while split_choice not in ['yes', 'no']:
        split_choice = input("Invalid choice. Please enter 'yes' or 'no': ").strip().lower()
    auto_split = (split_choice == 'yes')

    job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, temporal_constraints = get_user_input()

    if algo_choice == '1':
        print("\nSolving using Backtracking...")
        best_schedule, best_makespan = backtracking(job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, auto_split, temporal_constraints)
    else:
        print("\nSolving using Genetic Algorithm...")
        best_schedule, best_makespan = genetic_algorithm(job_durations, num_resources, precedence_constraints, resource_constraints, machine_capacities, auto_split, temporal_constraints)

    print("\n=== Results ===")
    if best_schedule:
        print(f"Minimum Makespan: {best_makespan}")
        for job, (start, end, resource) in sorted(best_schedule.items()):
            print(f"Job {job+1}: Starts at {start}, Ends at {end}, on Machine {resource+1}")
    else:
        print("No valid schedule found.")

    print("\nThank you for using the Job Scheduling Solver!")

except (EOFError, KeyboardInterrupt):
    print("\nInput terminated. Exiting...")
    sys.exit(0)

    