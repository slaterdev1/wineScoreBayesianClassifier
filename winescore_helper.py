import numpy as np

def compute_priors(y):
    priors = {}
    #print(y)
    #print(y.name)
    total_items = len(y)
    
    for value in y:
        if (y.name + '=' + str(value)) not in priors.keys():
            priors[(y.name + '=' + str(value))] = 1
        else:
            priors[(y.name + '=' + str(value))] += 1
            
    for key in priors.keys():
        priors[key] /= total_items
        
    return priors

def specific_class_conditional(x,xv,y,yv):
    prob = sum((x == xv) & (y == yv)) / sum(y == yv) 
    return prob

def class_conditional(X,y):
    # essentially loop over all series in X and get Specific Class Conditional
    probs = {}
    print(X)
    for column_name, series in X.items():
        print(column_name)
        x_values = series.unique()
        y_values = y.unique()
        for x_value in x_values:
            for y_value in y_values:
                name = column_name + "=" + str(x_value) + "|" + y.name + "=" + str(y_value)
                cd = specific_class_conditional(series, x_value, y, y_value)
                probs[name] = cd
        
        

   
    return probs

def posteriors(probs,priors,x):
    post_probs = {}
    
    labels = (x.index).tolist()
    keys = []
    
    for label in labels:
        keys.append(label + "=" + str(x[label]))
        
    print(keys)
    
    
    # P(A|B) = P(B|A)P(A) / P(B/A)P(A) + P(B/~A)P(~A)
    for prior_key in priors.keys():
        set_A = {prior_key: priors[prior_key]}
        set_not_A = priors.copy()
        set_not_A.pop(prior_key, None)
        
        print("A and ~A:", set_A, set_not_A)
        B_name = ','.join(keys)
        post_key = prior_key + "|" + B_name
        print(post_key)
        post_probs[post_key] = -1
        
        
        #Compute P(B|A)
        P_b_a = 1
        for key in keys:
            name = key + "|" + prior_key
            if name not in probs:
                post_probs[post_key] = 0.5
                break
            else:
                print("Compute Conditional")
                print(name)
                P_b_a *= probs[name]
        
        #Compute P(B|~A) and P(~A)
        P_b_not_a = 1
        P_not_a = 1
        for not_A_key in set_not_A.keys():
            P_not_a *= set_not_A[not_A_key]
            print(not_A_key)
            for key in keys:
                name = key + "|" + not_A_key
                if name not in probs:
                    break
                else:
                    print("Compute Conditional")
                    print(name)
                    P_b_not_a *= probs[name]
            
            
        #Compute P(~A)
        p_not_A = 1
        
        #Compute P(B|A)P(A)
        top = P_b_a * set_A[prior_key]
        
        #Compute P(B|~A)P(~A) + P(B|A)P(A)
        bottom = top + (P_b_not_a * P_not_a)
        
        post = top / bottom
        
        if post_probs[post_key] == -1:
            post_probs[post_key] = post
            
    return post_probs