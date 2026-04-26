Loaded models: [1m[[0m[32m'azure/gpt-4o'[0m[1m][0m                                                 
Received session ID: mcp-session-[93m36e74db8-e68b-4d1c-ab69-91125a4f8cd7[0m           
Negotiated protocol version: [1;36m2025[0m-[1;36m06[0m-[1;36m18[0m                                         
✅ Toolset aks_mcp                                                              
Using [1;36m3[0m datasources [1m([0mtoolsets[1m)[0m. To refresh: use flag `--refresh-toolsets`       
NO ENABLED LOGGING TOOLSET                                                      
Using model: azure/gpt-4o [1m([0m[1;36m128[0m,[1;36m000[0m total tokens, [1;36m16[0m,[1;36m384[0m output tokens[1m)[0m          
[1;33mThis tool uses AI to generate responses and may not always be accurate.[0m
[1;97mUser:[0m can user workloads without request or limit set with a sudden spike eat 
into kube-reserved? give a detailed explanation about this scenario and the 
possibilities. give the output in markdown format
Fetching new Azure AD token for Azure OpenAI authentication                     
Incomplete environment configuration for EnvironmentCredential. These variables 
are set: AZURE_TENANT_ID, AZURE_CLIENT_ID                                       
ManagedIdentityCredential will use workload identity with client_id:            
[93madd95581-5a12-472a-b982-fb1965cb9144[0m                                            
Request URL:                                                                    
[32m'https://login.microsoftonline.com/d12058fe-ecf4-454a-9a69-cef5686fc24f/oauth2/v[0m
[32m2.0/token'[0m                                                                      
Request method: [32m'[0m[1;33mPOST[0m[32m'[0m                                                          
Request headers:                                                                
    [32m'Content-Type'[0m: [32m'application/x-www-form-urlencoded'[0m                         
    [32m'User-Agent'[0m: [32m'azsdk-python-identity/1.25.3 Python/3.11.15 [0m                 
[32m([0m[32mLinux-5.15.0-1102-azure-x86_64-with-glibc2.36[0m[32m)[0m[32m'[0m                                
A body is sent with the request                                                 
Response status: [1;36m200[0m                                                            
Response headers:                                                               
    [32m'Cache-Control'[0m: [32m'no-store, no-cache'[0m                                       
    [32m'Pragma'[0m: [32m'no-cache'[0m                                                        
    [32m'Content-Type'[0m: [32m'application/json; [0m[32mcharset[0m[32m=[0m[32mutf[0m[32m-8'[0m                           
    [32m'Expires'[0m: [32m'-1'[0m                                                             
    [32m'Strict-Transport-Security'[0m: [32m'REDACTED'[0m                                     
    [32m'X-Content-Type-Options'[0m: [32m'REDACTED'[0m                                        
    [32m'x-ms-clientdata'[0m: [32m'REDACTED'[0m                                               
    [32m'P3P'[0m: [32m'REDACTED'[0m                                                           
    [32m'x-ms-request-id'[0m: [32m'29f35cba-7257-4619-b705-1c87f7bf0300'[0m                   
    [32m'x-ms-ests-server'[0m: [32m'REDACTED'[0m                                              
    [32m'x-ms-srs'[0m: [32m'REDACTED'[0m                                                      
    [32m'Content-Security-Policy-Report-Only'[0m: [32m'REDACTED'[0m                           
    [32m'X-XSS-Protection'[0m: [32m'REDACTED'[0m                                              
    [32m'Set-Cookie'[0m: [32m'REDACTED'[0m                                                    
    [32m'Date'[0m: [32m'Sun, 26 Apr 2026 19:00:33 GMT'[0m                                     
    [32m'Content-Length'[0m: [32m'2021'[0m                                                    
DefaultAzureCredential acquired a token from WorkloadIdentityCredential         
[1;96mAI:[0m To answer your question about whether user workloads without resource       
requests or limits can eat into `kube-reserved` during a sudden spike, I will   
break this into sub-problems to ensure a detailed and accurate explanation.     
                                                                                
### Sub-Problems to Address:                                                    
[1;36m1[0m. **Understand `kube-reserved` and its purpose**: Explain what `kube-reserved` 
is and how it is configured.                                                    
[1;36m2[0m. **Analyze the behavior of workloads without resource requests/limits**:      
Explain how Kubernetes schedules and manages such workloads.                    
[1;36m3[0m. **Investigate the interaction between workloads and `kube-reserved`**:       
Determine if and how workloads can consume resources reserved for Kubernetes    
system components.                                                              
[1;36m4[0m. **Explore scenarios where `kube-reserved` might be impacted**: Provide       
examples or conditions under which this could happen.                           
[1;36m5[0m. **Summarize the findings and provide recommendations**: Offer actionable     
insights to prevent such issues.                                                
                                                                                
I will now create a task list and begin addressing each sub-problem             
systematically.                                                                 
Running tool #[1;36m1[0m [1mTodoWrite[0m: Update investigation tasks                           
Task List:                                                                      
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| ID | Content                                                                  
| Status          |                                                             
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| [1;36m1[0m  | Explain what kube-reserved is and its purpose.                           
| [1m[[0m~[1m][0m in_progress |                                                             
| [1;36m2[0m  | Explain how Kubernetes schedules and manages workloads without resource  
requests or limits.                                | [1m[[0m [1m][0m pending     |          
| [1;36m3[0m  | Analyze the interaction between workloads and kube-reserved to determine 
if workloads can consume kube-reserved resources. | [1m[[0m [1m][0m pending     |           
| [1;36m4[0m  | Explore scenarios where kube-reserved might be impacted by workloads     
without resource requests or limits.                  | [1m[[0m [1m][0m pending     |       
| [1;36m5[0m  | Summarize findings and provide recommendations to prevent issues with    
kube-reserved.                                       | [1m[[0m [1m][0m pending     |        
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
  [2mFinished #[0m[1;2;36m1[0m[2m in [0m[1;2;36m0.[0m[2m00s, output length: [0m[1;2;36m837[0m[2m characters [0m[1;2m([0m[1;2;36m13[0m[2m lines[0m[1;2m)[0m[2m - [0m[2;35m/[0m[2;95mshow[0m[2m [0m[1;2;36m1[0m[2m to [0m  
[2mview contents[0m                                                                   
The AI requested [1;36m1[0m tool [1;35mcall[0m[1m([0ms[1m)[0m.                                                
                                                                                
[1;96mAI:[0m ### What is `kube-reserved` and its purpose?                                
                                                                                
`kube-reserved` is a resource reservation mechanism in Kubernetes designed to   
ensure that critical system components running on a node [1m([0me.g., kubelet,        
container runtime, and other system daemons[1m)[0m have sufficient resources to       
operate reliably. It is configured at the node level and typically includes     
reservations for CPU, memory, and ephemeral storage.                            
                                                                                
#### Key Points:                                                                
- **Purpose**: Prevent resource contention between user workloads and system    
components by reserving a portion of the node's resources exclusively for       
Kubernetes system processes.                                                    
- **Configuration**: Defined in the kubelet configuration file or via           
command-line flags [1m([0m`--kube-reserved`[1m)[0m.                                         
- **Scope**: Applies only to system components; user workloads are not supposed 
to consume these reserved resources.                                            
                                                                                
I will now proceed to the next task: explaining how Kubernetes schedules and    
manages workloads without resource requests or limits.                          
Running tool #[1;36m2[0m [1mTodoWrite[0m: Update investigation tasks                           
Task List:                                                                      
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| ID | Content                                                                  
| Status          |                                                             
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| [1;36m1[0m  | Explain what kube-reserved is and its purpose.                           
| [1m[[0m✓[1m][0m completed   |                                                             
| [1;36m2[0m  | Explain how Kubernetes schedules and manages workloads without resource  
requests or limits.                                | [1m[[0m~[1m][0m in_progress |          
| [1;36m3[0m  | Analyze the interaction between workloads and kube-reserved to determine 
if workloads can consume kube-reserved resources. | [1m[[0m [1m][0m pending     |           
| [1;36m4[0m  | Explore scenarios where kube-reserved might be impacted by workloads     
without resource requests or limits.                  | [1m[[0m [1m][0m pending     |       
| [1;36m5[0m  | Summarize findings and provide recommendations to prevent issues with    
kube-reserved.                                       | [1m[[0m [1m][0m pending     |        
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
  [2mFinished #[0m[1;2;36m2[0m[2m in [0m[1;2;36m0.[0m[2m00s, output length: [0m[1;2;36m837[0m[2m characters [0m[1;2m([0m[1;2;36m13[0m[2m lines[0m[1;2m)[0m[2m - [0m[2;35m/[0m[2;95mshow[0m[2m [0m[1;2;36m2[0m[2m to [0m  
[2mview contents[0m                                                                   
The AI requested [1;36m1[0m tool [1;35mcall[0m[1m([0ms[1m)[0m.                                                
                                                                                
[1;96mAI:[0m ### How Kubernetes Schedules and Manages Workloads Without Resource Requests
or Limits                                                                       
                                                                                
In Kubernetes, workloads [1m([0mpods[1m)[0m without resource requests or limits are treated 
differently compared to those with defined resource specifications.             
                                                                                
#### Key Points:                                                                
[1;36m1[0m. **No Resource Requests**:                                                    
   - Pods without resource requests are assigned a **default request** value if 
a `LimitRange` is defined in the namespace.                                     
   - If no `LimitRange` is defined, the pod is scheduled without any guaranteed 
resources, meaning it competes for resources on a best-effort basis.            
                                                                                
[1;36m2[0m. **No Resource Limits**:                                                      
   - Pods without resource limits can consume as much CPU and memory as         
available on the node, potentially leading to resource contention.              
                                                                                
[1;36m3[0m. **Scheduling Behavior**:                                                     
   - The Kubernetes scheduler places pods on nodes based on available capacity. 
For pods without requests, the scheduler assumes they require minimal resources,
which can lead to overcommitment.                                               
                                                                                
[1;36m4[0m. **Runtime Behavior**:                                                        
   - Once running, these pods can consume resources beyond their initial        
assumptions, potentially impacting other workloads and system components.       
                                                                                
I will now analyze the interaction between such workloads and `kube-reserved` to
determine if they can consume reserved resources.                               
Running tool #[1;36m3[0m [1mTodoWrite[0m: Update investigation tasks                           
Task List:                                                                      
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| ID | Content                                                                  
| Status          |                                                             
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| [1;36m1[0m  | Explain what kube-reserved is and its purpose.                           
| [1m[[0m✓[1m][0m completed   |                                                             
| [1;36m2[0m  | Explain how Kubernetes schedules and manages workloads without resource  
requests or limits.                                | [1m[[0m✓[1m][0m completed   |          
| [1;36m3[0m  | Analyze the interaction between workloads and kube-reserved to determine 
if workloads can consume kube-reserved resources. | [1m[[0m~[1m][0m in_progress |           
| [1;36m4[0m  | Explore scenarios where kube-reserved might be impacted by workloads     
without resource requests or limits.                  | [1m[[0m [1m][0m pending     |       
| [1;36m5[0m  | Summarize findings and provide recommendations to prevent issues with    
kube-reserved.                                       | [1m[[0m [1m][0m pending     |        
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
  [2mFinished #[0m[1;2;36m3[0m[2m in [0m[1;2;36m0.[0m[2m00s, output length: [0m[1;2;36m837[0m[2m characters [0m[1;2m([0m[1;2;36m13[0m[2m lines[0m[1;2m)[0m[2m - [0m[2;35m/[0m[2;95mshow[0m[2m [0m[1;2;36m3[0m[2m to [0m  
[2mview contents[0m                                                                   
The AI requested [1;36m1[0m tool [1;35mcall[0m[1m([0ms[1m)[0m.                                                
                                                                                
[1;96mAI:[0m ### Interaction Between Workloads and `kube-reserved`                       
                                                                                
Workloads without resource requests or limits can potentially consume resources 
reserved for Kubernetes system components [1m([0m`kube-reserved`[1m)[0m under certain       
conditions:                                                                     
                                                                                
#### Key Points:                                                                
[1;36m1[0m. **Resource Enforcement**:                                                    
   - `kube-reserved` is not enforced by cgroups or any hard limits. It is a     
logical reservation, meaning it relies on proper configuration and scheduling to
ensure system components have sufficient resources.                             
   - If the node is under heavy load, workloads without limits can consume      
resources beyond their fair share, including those logically reserved for       
`kube-reserved`.                                                                
                                                                                
[1;36m2[0m. **Best-Effort Pods**:                                                        
   - Pods without requests are treated as **BestEffort QoS**. These pods have   
the lowest priority and are the first to be throttled or evicted during resource
contention.                                                                     
   - However, before eviction, they can still consume resources, potentially    
impacting system components.                                                    
                                                                                
[1;36m3[0m. **System Component Starvation**:                                             
   - If workloads consume all available CPU or memory, system components like   
the kubelet or container runtime may not have enough resources to function      
properly, leading to node instability.                                          
                                                                                
I will now explore specific scenarios where `kube-reserved` might be impacted by
such workloads.                                                                 
Running tool #[1;36m4[0m [1mTodoWrite[0m: Update investigation tasks                           
Task List:                                                                      
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| ID | Content                                                                  
| Status          |                                                             
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| [1;36m1[0m  | Explain what kube-reserved is and its purpose.                           
| [1m[[0m✓[1m][0m completed   |                                                             
| [1;36m2[0m  | Explain how Kubernetes schedules and manages workloads without resource  
requests or limits.                                | [1m[[0m✓[1m][0m completed   |          
| [1;36m3[0m  | Analyze the interaction between workloads and kube-reserved to determine 
if workloads can consume kube-reserved resources. | [1m[[0m✓[1m][0m completed   |           
| [1;36m4[0m  | Explore scenarios where kube-reserved might be impacted by workloads     
without resource requests or limits.                  | [1m[[0m~[1m][0m in_progress |       
| [1;36m5[0m  | Summarize findings and provide recommendations to prevent issues with    
kube-reserved.                                       | [1m[[0m [1m][0m pending     |        
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
  [2mFinished #[0m[1;2;36m4[0m[2m in [0m[1;2;36m0.[0m[2m00s, output length: [0m[1;2;36m837[0m[2m characters [0m[1;2m([0m[1;2;36m13[0m[2m lines[0m[1;2m)[0m[2m - [0m[2;35m/[0m[2;95mshow[0m[2m [0m[1;2;36m4[0m[2m to [0m  
[2mview contents[0m                                                                   
The AI requested [1;36m1[0m tool [1;35mcall[0m[1m([0ms[1m)[0m.                                                
                                                                                
[1;96mAI:[0m ### Scenarios Where `kube-reserved` Might Be Impacted                       
                                                                                
[1;36m1[0m. **High Node Utilization**:                                                   
   - If a node is running multiple workloads without resource requests or       
limits, these workloads can consume all available CPU and memory.               
   - This can lead to resource starvation for system components, as             
`kube-reserved` is not enforced by hard limits.                                 
                                                                                
[1;36m2[0m. **Sudden Resource Spikes**:                                                  
   - Workloads with unpredictable resource usage [1m([0me.g., batch jobs, data        
processing[1m)[0m can cause sudden spikes in CPU or memory consumption.               
   - Without limits, these spikes can encroach on resources reserved for        
Kubernetes system components.                                                   
                                                                                
[1;36m3[0m. **Misconfigured Nodes**:                                                     
   - Nodes with insufficient `kube-reserved` values or no `kube-reserved`       
configuration are more vulnerable to resource contention.                       
   - In such cases, even moderate workloads can impact system components.       
                                                                                
[1;36m4[0m. **BestEffort Pods**:                                                         
   - BestEffort pods [1m([0mno requests or limits[1m)[0m are scheduled without guaranteed   
resources. During high load, they can consume resources meant for               
`kube-reserved` until they are throttled or evicted.                            
                                                                                
I will now summarize the findings and provide recommendations to prevent issues 
with `kube-reserved`.                                                           
Running tool #[1;36m5[0m [1mTodoWrite[0m: Update investigation tasks                           
Task List:                                                                      
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| ID | Content                                                                  
| Status          |                                                             
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
| [1;36m1[0m  | Explain what kube-reserved is and its purpose.                           
| [1m[[0m✓[1m][0m completed   |                                                             
| [1;36m2[0m  | Explain how Kubernetes schedules and manages workloads without resource  
requests or limits.                                | [1m[[0m✓[1m][0m completed   |          
| [1;36m3[0m  | Analyze the interaction between workloads and kube-reserved to determine 
if workloads can consume kube-reserved resources. | [1m[[0m✓[1m][0m completed   |           
| [1;36m4[0m  | Explore scenarios where kube-reserved might be impacted by workloads     
without resource requests or limits.                  | [1m[[0m✓[1m][0m completed   |       
| [1;36m5[0m  | Summarize findings and provide recommendations to prevent issues with    
kube-reserved.                                       | [1m[[0m~[1m][0m in_progress |        
+----+--------------------------------------------------------------------------
--------------------------------------------------+-----------------+           
  [2mFinished #[0m[1;2;36m5[0m[2m in [0m[1;2;36m0.[0m[2m00s, output length: [0m[1;2;36m837[0m[2m characters [0m[1;2m([0m[1;2;36m13[0m[2m lines[0m[1;2m)[0m[2m - [0m[2;35m/[0m[2;95mshow[0m[2m [0m[1;2;36m5[0m[2m to [0m  
[2mview contents[0m                                                                   
The AI requested [1;36m1[0m tool [1;35mcall[0m[1m([0ms[1m)[0m.                                                
                                                                                
[1;96mAI:[0m ### Summary and Recommendations                                             
                                                                                
#### Findings:                                                                  
[1;36m1[0m. **`kube-reserved` Purpose**:                                                 
   - Ensures critical Kubernetes system components have sufficient resources to 
operate reliably.                                                               
   - Configured as a logical reservation, not enforced by hard limits.          
                                                                                
[1;36m2[0m. **Workloads Without Requests or Limits**:                                    
   - Treated as BestEffort QoS, with no guaranteed resources.                   
   - Can consume all available resources on a node, including those logically   
reserved for `kube-reserved`.                                                   
                                                                                
[1;36m3[0m. **Impact on `kube-reserved`**:                                               
   - High node utilization or sudden resource spikes can lead to resource       
contention.                                                                     
   - Misconfigured or insufficient `kube-reserved` values exacerbate the issue. 
                                                                                
[1;36m4[0m. **Scenarios of Concern**:                                                    
   - Nodes with multiple BestEffort pods.                                       
   - Workloads with unpredictable resource usage.                               
   - Nodes lacking proper `kube-reserved` configuration.                        
                                                                                
#### Recommendations:                                                           
[1;36m1[0m. **Set Resource Requests and Limits**:                                        
   - Define resource requests and limits for all workloads to ensure fair       
resource allocation and prevent overcommitment.                                 
                                                                                
[1;36m2[0m. **Configure `kube-reserved` Properly**:                                      
   - Reserve adequate CPU, memory, and storage for system components based on   
node size and workload characteristics.                                         
                                                                                
[1;36m3[0m. **Use `LimitRange` and `ResourceQuota`**:                                    
   - Enforce default resource requests and limits in namespaces to prevent      
BestEffort pods from consuming excessive resources.                             
                                                                                
[1;36m4[0m. **Monitor Node Utilization**:                                                
   - Use monitoring tools to track resource usage and identify nodes under high 
load.                                                                           
                                                                                
[1;36m5[0m. **Eviction Policies**:                                                       
   - Configure eviction thresholds to ensure system components are prioritized  
during resource contention.                                                     
                                                                                
By implementing these measures, you can prevent workloads without resource      
requests or limits from impacting `kube-reserved` and ensure stable cluster     
operations.                                                                     
Running tool #[1;36m6[0m [1mTodoWrite[0m: Update investigation tasks                           
Task List:                                                                      
+----+--------------------------------------------------------------------------
--------------------------------------------------+---------------+             
| ID | Content                                                                  
| Status        |                                                               
+----+--------------------------------------------------------------------------
--------------------------------------------------+---------------+             
| [1;36m1[0m  | Explain what kube-reserved is and its purpose.                           
| [1m[[0m✓[1m][0m completed |                                                               
| [1;36m2[0m  | Explain how Kubernetes schedules and manages workloads without resource  
requests or limits.                                | [1m[[0m✓[1m][0m completed |            
| [1;36m3[0m  | Analyze the interaction between workloads and kube-reserved to determine 
if workloads can consume kube-reserved resources. | [1m[[0m✓[1m][0m completed |             
| [1;36m4[0m  | Explore scenarios where kube-reserved might be impacted by workloads     
without resource requests or limits.                  | [1m[[0m✓[1m][0m completed |         
| [1;36m5[0m  | Summarize findings and provide recommendations to prevent issues with    
kube-reserved.                                       | [1m[[0m✓[1m][0m completed |          
+----+--------------------------------------------------------------------------
--------------------------------------------------+---------------+             
  [2mFinished #[0m[1;2;36m6[0m[2m in [0m[1;2;36m0.[0m[2m00s, output length: [0m[1;2;36m837[0m[2m characters [0m[1;2m([0m[1;2;36m13[0m[2m lines[0m[1;2m)[0m[2m - [0m[2;35m/[0m[2;95mshow[0m[2m [0m[1;2;36m6[0m[2m to [0m  
[2mview contents[0m                                                                   
The AI requested [1;36m1[0m tool [1;35mcall[0m[1m([0ms[1m)[0m.                                                
                                                                                
[1;96mAI:[0m                                 [1mMarkdown Output[0m                                 

[40m                                                                                [0m
[40m [0m[97;40m# Can User Workloads Without Requests or Limits Impact `kube-reserved`?[0m[40m       [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[37;40m## Findings[0m[40m                                                                   [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[37;40m### 1. What is `kube-reserved`?[0m[40m                                               [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**Purpose**[0m[97;40m:[0m[97;40m [0m[97;40mEnsures[0m[97;40m [0m[97;40mcritical[0m[97;40m [0m[97;40mKubernetes[0m[97;40m [0m[97;40msystem[0m[97;40m [0m[97;40mcomponents[0m[97;40m [0m[97;40m(e.g.,[0m[97;40m [0m[97;40mkubelet,[0m[97;40m [0m[40m [0m[40m [0m
[40m [0m[97;40mcontainer[0m[97;40m [0m[97;40mruntime)[0m[97;40m [0m[97;40mhave[0m[97;40m [0m[97;40msufficient[0m[97;40m [0m[97;40mresources[0m[97;40m [0m[97;40mto[0m[97;40m [0m[97;40moperate[0m[97;40m [0m[97;40mreliably.[0m[40m             [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**Configuration**[0m[97;40m:[0m[97;40m [0m[97;40mDefined[0m[97;40m [0m[97;40min[0m[97;40m [0m[97;40mthe[0m[97;40m [0m[97;40mkubelet[0m[97;40m [0m[97;40mconfiguration[0m[97;40m [0m[97;40mfile[0m[97;40m [0m[97;40mor[0m[97;40m [0m[97;40mvia[0m[97;40m [0m[40m        [0m[40m [0m
[40m [0m[93;40m`--kube-reserved`[0m[97;40m [0m[97;40mflags.[0m[40m                                                      [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**Scope**[0m[97;40m:[0m[97;40m [0m[97;40mLogical[0m[97;40m [0m[97;40mreservation,[0m[97;40m [0m[97;40mnot[0m[97;40m [0m[97;40menforced[0m[97;40m [0m[97;40mby[0m[97;40m [0m[97;40mhard[0m[97;40m [0m[97;40mlimits.[0m[40m                [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[37;40m### 2. Behavior of Workloads Without Requests or Limits[0m[40m                       [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**No Requests**[0m[97;40m:[0m[97;40m [0m[97;40mTreated[0m[97;40m [0m[97;40mas[0m[97;40m [0m[97;40mBestEffort[0m[97;40m [0m[97;40mQoS,[0m[97;40m [0m[97;40mwith[0m[97;40m [0m[97;40mno[0m[97;40m [0m[97;40mguaranteed[0m[97;40m [0m[97;40mresources.[0m[40m   [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**No Limits**[0m[97;40m:[0m[97;40m [0m[97;40mCan[0m[97;40m [0m[97;40mconsume[0m[97;40m [0m[97;40mas[0m[97;40m [0m[97;40mmuch[0m[97;40m [0m[97;40mCPU[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40mmemory[0m[97;40m [0m[97;40mas[0m[97;40m [0m[97;40mavailable[0m[97;40m [0m[97;40mon[0m[97;40m [0m[97;40mthe[0m[97;40m [0m[97;40mnode.[0m[40m [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**Scheduling**[0m[97;40m:[0m[97;40m [0m[97;40mScheduler[0m[97;40m [0m[97;40massumes[0m[97;40m [0m[97;40mminimal[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40mrequirements,[0m[97;40m [0m[97;40mleading[0m[97;40m [0m[97;40mto[0m[97;40m [0m[40m [0m
[40m [0m[97;40mpotential[0m[97;40m [0m[97;40movercommitment.[0m[40m                                                     [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**Runtime**[0m[97;40m:[0m[97;40m [0m[97;40mCan[0m[97;40m [0m[97;40mconsume[0m[97;40m [0m[97;40mresources[0m[97;40m [0m[97;40mbeyond[0m[97;40m [0m[97;40mtheir[0m[97;40m [0m[97;40mfair[0m[97;40m [0m[97;40mshare,[0m[97;40m [0m[97;40mimpacting[0m[97;40m [0m[97;40mother[0m[97;40m [0m[40m [0m
[40m [0m[97;40mworkloads[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40msystem[0m[97;40m [0m[97;40mcomponents.[0m[40m                                              [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[37;40m### 3. Interaction Between Workloads and `kube-reserved`[0m[40m                      [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**Resource Enforcement**[0m[97;40m:[0m[97;40m [0m[93;40m`kube-reserved`[0m[97;40m [0m[97;40mis[0m[97;40m [0m[97;40mnot[0m[97;40m [0m[97;40menforced[0m[97;40m [0m[97;40mby[0m[97;40m [0m[97;40mcgroups[0m[97;40m [0m[97;40mor[0m[97;40m [0m[97;40mhard[0m[40m [0m
[40m [0m[97;40mlimits.[0m[40m                                                                       [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**BestEffort Pods**[0m[97;40m:[0m[97;40m [0m[97;40mCan[0m[97;40m [0m[97;40mconsume[0m[97;40m [0m[97;40mresources[0m[97;40m [0m[97;40mmeant[0m[97;40m [0m[97;40mfor[0m[97;40m [0m[93;40m`kube-reserved`[0m[97;40m [0m[97;40muntil[0m[97;40m [0m[40m [0m[40m [0m
[40m [0m[97;40mthrottled[0m[97;40m [0m[97;40mor[0m[97;40m [0m[97;40mevicted.[0m[40m                                                         [0m[40m [0m
[40m [0m[96;40m-[0m[97;40m [0m[1;97;40m**System Component Starvation**[0m[97;40m:[0m[97;40m [0m[97;40mHigh[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40musage[0m[97;40m [0m[97;40mby[0m[97;40m [0m[97;40mworkloads[0m[97;40m [0m[97;40mcan[0m[97;40m [0m[97;40mlead[0m[97;40m [0m[97;40mt[0m[40m [0m
[40m [0m[97;40mnode[0m[97;40m [0m[97;40minstability.[0m[40m                                                             [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[37;40m### 4. Scenarios Where `kube-reserved` Might Be Impacted[0m[40m                      [0m[40m [0m
[40m [0m[96;40m1.[0m[97;40m [0m[1;97;40m**High Node Utilization**[0m[97;40m:[0m[97;40m [0m[97;40mMultiple[0m[97;40m [0m[97;40mworkloads[0m[97;40m [0m[97;40mwithout[0m[97;40m [0m[97;40mrequests[0m[97;40m [0m[97;40mor[0m[97;40m [0m[97;40mlimits[0m[97;40m [0m[97;40mca[0m[40m [0m
[40m [0m[97;40mconsume[0m[97;40m [0m[97;40mall[0m[97;40m [0m[97;40mresources.[0m[40m                                                        [0m[40m [0m
[40m [0m[96;40m2.[0m[97;40m [0m[1;97;40m**Sudden Resource Spikes**[0m[97;40m:[0m[97;40m [0m[97;40mUnpredictable[0m[97;40m [0m[97;40mworkloads[0m[97;40m [0m[97;40m(e.g.,[0m[97;40m [0m[97;40mbatch[0m[97;40m [0m[97;40mjobs)[0m[97;40m [0m[97;40mcan[0m[97;40m [0m[40m [0m
[40m [0m[97;40mencroach[0m[97;40m [0m[97;40mon[0m[97;40m [0m[93;40m`kube-reserved`[0m[97;40m.[0m[40m                                                  [0m[40m [0m
[40m [0m[96;40m3.[0m[97;40m [0m[1;97;40m**Misconfigured Nodes**[0m[97;40m:[0m[97;40m [0m[97;40mInsufficient[0m[97;40m [0m[97;40mor[0m[97;40m [0m[97;40mmissing[0m[97;40m [0m[93;40m`kube-reserved`[0m[97;40m [0m[97;40mvalues[0m[97;40m [0m[40m   [0m[40m [0m
[40m [0m[97;40mexacerbate[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40mcontention.[0m[40m                                               [0m[40m [0m
[40m [0m[96;40m4.[0m[97;40m [0m[1;97;40m**BestEffort Pods**[0m[97;40m:[0m[97;40m [0m[97;40mThese[0m[97;40m [0m[97;40mpods[0m[97;40m [0m[97;40mare[0m[97;40m [0m[97;40mscheduled[0m[97;40m [0m[97;40mwithout[0m[97;40m [0m[97;40mguaranteed[0m[97;40m [0m[97;40mresources,[0m[40m [0m
[40m [0m[97;40mimpacting[0m[97;40m [0m[97;40msystem[0m[97;40m [0m[97;40mcomponents[0m[97;40m [0m[97;40mduring[0m[97;40m [0m[97;40mhigh[0m[97;40m [0m[97;40mload.[0m[40m                                 [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[97;40m---[0m[40m                                                                           [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[37;40m## Recommendations[0m[40m                                                            [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[96;40m1.[0m[97;40m [0m[1;97;40m**Set Resource Requests and Limits**[0m[97;40m:[0m[40m                                      [0m[40m [0m
[40m [0m[97;40m   [0m[96;40m-[0m[97;40m [0m[97;40mDefine[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40mrequests[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40mlimits[0m[97;40m [0m[97;40mfor[0m[97;40m [0m[97;40mall[0m[97;40m [0m[97;40mworkloads[0m[97;40m [0m[97;40mto[0m[97;40m [0m[97;40mensure[0m[97;40m [0m[97;40mfair[0m[97;40m [0m[40m    [0m[40m [0m
[40m [0m[97;40mresource[0m[97;40m [0m[97;40mallocation.[0m[40m                                                          [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[96;40m2.[0m[97;40m [0m[1;97;40m**Configure `kube-reserved` Properly**[0m[97;40m:[0m[40m                                    [0m[40m [0m
[40m [0m[97;40m   [0m[96;40m-[0m[97;40m [0m[97;40mReserve[0m[97;40m [0m[97;40madequate[0m[97;40m [0m[97;40mCPU,[0m[97;40m [0m[97;40mmemory,[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40mstorage[0m[97;40m [0m[97;40mfor[0m[97;40m [0m[97;40msystem[0m[97;40m [0m[97;40mcomponents[0m[97;40m [0m[97;40mbased[0m[97;40m [0m[97;40mon[0m[97;40m [0m[40m [0m
[40m [0m[97;40mnode[0m[97;40m [0m[97;40msize[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40mworkload[0m[97;40m [0m[97;40mcharacteristics.[0m[40m                                       [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[96;40m3.[0m[97;40m [0m[1;97;40m**Use `LimitRange` and `ResourceQuota`**[0m[97;40m:[0m[40m                                  [0m[40m [0m
[40m [0m[97;40m   [0m[96;40m-[0m[97;40m [0m[97;40mEnforce[0m[97;40m [0m[97;40mdefault[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40mrequests[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40mlimits[0m[97;40m [0m[97;40min[0m[97;40m [0m[97;40mnamespaces[0m[97;40m [0m[97;40mto[0m[97;40m [0m[97;40mprevent[0m[97;40m [0m[40m   [0m[40m [0m
[40m [0m[97;40mBestEffort[0m[97;40m [0m[97;40mpods[0m[97;40m [0m[97;40mfrom[0m[97;40m [0m[97;40mconsuming[0m[97;40m [0m[97;40mexcessive[0m[97;40m [0m[97;40mresources.[0m[40m                           [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[96;40m4.[0m[97;40m [0m[1;97;40m**Monitor Node Utilization**[0m[97;40m:[0m[40m                                              [0m[40m [0m
[40m [0m[97;40m   [0m[96;40m-[0m[97;40m [0m[97;40mUse[0m[97;40m [0m[97;40mmonitoring[0m[97;40m [0m[97;40mtools[0m[97;40m [0m[97;40mto[0m[97;40m [0m[97;40mtrack[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40musage[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40midentify[0m[97;40m [0m[97;40mnodes[0m[97;40m [0m[97;40munder[0m[97;40m [0m[97;40mhig[0m[40m [0m
[40m [0m[97;40mload.[0m[40m                                                                         [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[96;40m5.[0m[97;40m [0m[1;97;40m**Eviction Policies**[0m[97;40m:[0m[40m                                                     [0m[40m [0m
[40m [0m[97;40m   [0m[96;40m-[0m[97;40m [0m[97;40mConfigure[0m[97;40m [0m[97;40meviction[0m[97;40m [0m[97;40mthresholds[0m[97;40m [0m[97;40mto[0m[97;40m [0m[97;40mensure[0m[97;40m [0m[97;40msystem[0m[97;40m [0m[97;40mcomponents[0m[97;40m [0m[97;40mare[0m[97;40m [0m[97;40mprioritized[0m[40m [0m
[40m [0m[97;40mduring[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[97;40mcontention.[0m[40m                                                   [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[97;40m---[0m[40m                                                                           [0m[40m [0m
[40m [0m[40m                                                                              [0m[40m [0m
[40m [0m[97;40mBy[0m[97;40m [0m[97;40mimplementing[0m[97;40m [0m[97;40mthese[0m[97;40m [0m[97;40mmeasures,[0m[97;40m [0m[97;40myou[0m[97;40m [0m[97;40mcan[0m[97;40m [0m[97;40mprevent[0m[97;40m [0m[97;40mworkloads[0m[97;40m [0m[97;40mwithout[0m[97;40m [0m[97;40mresource[0m[97;40m [0m[40m   [0m[40m [0m
[40m [0m[97;40mrequests[0m[97;40m [0m[97;40mor[0m[97;40m [0m[97;40mlimits[0m[97;40m [0m[97;40mfrom[0m[97;40m [0m[97;40mimpacting[0m[97;40m [0m[93;40m`kube-reserved`[0m[97;40m [0m[97;40mand[0m[97;40m [0m[97;40mensure[0m[97;40m [0m[97;40mstable[0m[97;40m [0m[97;40mcluster[0m[97;40m [0m[40m  [0m[40m [0m
[40m [0m[97;40moperations.[0m[40m                                                                   [0m[40m [0m
[40m                                                                                [0m
