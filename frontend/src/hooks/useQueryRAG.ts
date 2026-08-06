import { useMutation } from '@tanstack/react-query';
import { queryService } from '../services/queryService';
import { QueryResponseData } from '../types';
import { toast } from 'sonner';

export const useQueryRAG = () => {
  return useMutation<QueryResponseData, Error, string>({
    mutationFn: (question: string) => queryService.askQuestion(question),
    onError: (error: Error) => {
      toast.error(`AI query failed: ${error.message}`);
    },
  });
};
