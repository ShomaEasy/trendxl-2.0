import { useEffect, useState, useCallback } from 'react';
import { Box, Text, Button, HStack, VStack, Icon, Badge } from '@chakra-ui/react';
import { AlertCircle, CreditCard, Check, Gift, Clock, Sparkles, Settings } from 'lucide-react';
import {
  checkSubscriptionStatus,
  createPublicPaymentLink,
  getFreeTrialInfo,
  createCustomerPortalSession,
  type SubscriptionStatus,
  type FreeTrialInfo,
} from '@/services/subscriptionService';
import { useAuth } from '@/contexts/AuthContext';
import { useAutoRefresh, calculateTimeUntilReset, formatTimeRemaining } from '@/hooks/useAutoRefresh';

interface UnifiedSubscriptionBannerProps {
  refreshTrigger?: number;
}

export function UnifiedSubscriptionBanner({ refreshTrigger }: UnifiedSubscriptionBannerProps = {}) {
  const { user } = useAuth();
  const [subscriptionStatus, setSubscriptionStatus] = useState<SubscriptionStatus | null>(null);
  const [freeTrialInfo, setFreeTrialInfo] = useState<FreeTrialInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [creatingPayment, setCreatingPayment] = useState(false);
  const [resetTime, setResetTime] = useState('');

  // Memoize loading functions
  const loadSubscriptionStatus = useCallback(async () => {
    try {
      const status = await checkSubscriptionStatus();
      setSubscriptionStatus(status);
    } catch (error) {
      console.error('Failed to load subscription status:', error);
      setSubscriptionStatus({
        has_active_subscription: false,
        subscription_status: 'none',
        subscription_end_date: null,
      });
    }
  }, []);

  const loadFreeTrialInfo = useCallback(async () => {
    try {
      const info = await getFreeTrialInfo();
      setFreeTrialInfo(info);
      console.log('✅ UnifiedBanner: Free trial info loaded', info);
    } catch (error) {
      console.error('Failed to load free trial info:', error);
      setFreeTrialInfo({
        can_use_free_trial: true,
        today_count: 0,
        daily_limit: 1,
        total_free_analyses: 0,
        has_subscription: false,
        is_admin: false,
        message: 'You get 1 free profile analysis per day!',
      });
    }
  }, []);

  // Update reset time
  const updateResetTime = useCallback(() => {
    const { hours, minutes } = calculateTimeUntilReset();
    setResetTime(formatTimeRemaining(hours, minutes));
  }, []);

  // Initial load
  useEffect(() => {
    if (user) {
      Promise.all([loadSubscriptionStatus(), loadFreeTrialInfo()]).finally(() => {
        setLoading(false);
        updateResetTime();
      });
    }
  }, [user, loadSubscriptionStatus, loadFreeTrialInfo, updateResetTime]);

  // Auto-refresh when refreshTrigger changes (after successful analysis)
  useEffect(() => {
    if (user && refreshTrigger) {
      console.log('🔄 UnifiedBanner: Refreshing after analysis');
      loadFreeTrialInfo();
    }
  }, [refreshTrigger, user, loadFreeTrialInfo]);

  // Auto-refresh every 60 seconds
  useAutoRefresh(() => {
    loadSubscriptionStatus();
    loadFreeTrialInfo();
    updateResetTime();
  }, 60000, !!user);

  const handleSubscribe = async () => {
    try {
      setCreatingPayment(true);

      const successUrl = `${window.location.origin}/subscription/success`;
      const cancelUrl = window.location.origin;

      const paymentLink = await createPublicPaymentLink(
        user?.email,
        successUrl,
        cancelUrl
      );

      window.location.href = paymentLink.payment_url;
    } catch (error) {
      console.error('Failed to create payment link:', error);
      alert('Failed to create payment link. Please try again.');
    } finally {
      setCreatingPayment(false);
    }
  };

  const handleManageSubscription = async () => {
    try {
      setCreatingPayment(true);
      const portalUrl = await createCustomerPortalSession();
      window.location.href = portalUrl;
    } catch (error) {
      console.error('Failed to open customer portal:', error);
      alert('Failed to open subscription management. Please try again.');
    } finally {
      setCreatingPayment(false);
    }
  };

  // Don't show banner if user is not authenticated or loading
  if (!user || loading) {
    return null;
  }

  // Show active subscription banner
  if (subscriptionStatus?.has_active_subscription || freeTrialInfo?.has_subscription) {
    return (
      <Box
        bg="green.50"
        border="2px"
        borderColor="green.400"
        borderRadius="lg"
        p={4}
        mb={4}
        className="animate-fade-in"
      >
        <HStack gap={4} justify="space-between" align="center" flexWrap="wrap">
          {/* Left side: Status */}
          <HStack gap={3} flex={1}>
            <Icon as={Check} color="green.500" boxSize={5} />
            <Text fontWeight="bold" color="green.700" fontSize="sm">
              ✨ Premium Active - Unlimited Scans
            </Text>
          </HStack>

          {/* Right side: Manage button */}
          <Button
            onClick={handleManageSubscription}
            isLoading={creatingPayment}
            colorScheme="green"
            variant="solid"
            size="sm"
            flexShrink={0}
            bg="green.600"
            color="white"
            _hover={{ bg: "green.700" }}
          >
            <HStack gap={2}>
              <Icon as={Settings} boxSize={4} />
              <span>Manage Subscription</span>
            </HStack>
          </Button>
        </HStack>
      </Box>
    );
  }

  // Calculate trial status
  const canUseTrial = freeTrialInfo?.can_use_free_trial ?? false;
  const usedToday = freeTrialInfo?.today_count ?? 0;
  const dailyLimit = freeTrialInfo?.daily_limit ?? 1;
  const remaining = canUseTrial ? dailyLimit - usedToday : 0;
  
  return (
    <Box
      bg={canUseTrial ? "purple.50" : "orange.50"}
      border="2px"
      borderColor={canUseTrial ? "purple.400" : "orange.400"}
      borderRadius="lg"
      p={4}
      mb={4}
      className="animate-fade-in"
    >
      <HStack gap={4} justify="space-between" align="center" flexWrap="wrap">
        {/* Left side: Icon + Status + Counter */}
        <HStack gap={3} flex={1} minW="200px">
          <Icon 
            as={canUseTrial ? Gift : AlertCircle} 
            color={canUseTrial ? "purple.500" : "orange.500"} 
            boxSize={5} 
          />
          <VStack align="start" gap={1} flex={1}>
            <HStack gap={2} flexWrap="wrap">
              <Text fontWeight="bold" color={canUseTrial ? "purple.700" : "orange.700"} fontSize="sm">
                {canUseTrial ? "🎁 Free Trial Available" : "Subscription Required"}
              </Text>
              <Badge colorScheme={canUseTrial ? "purple" : "orange"} variant="solid">
                {remaining}/{dailyLimit} {canUseTrial ? "Free Today" : "Used Today"}
              </Badge>
            </HStack>
            
            {/* Reset Timer */}
            {!canUseTrial && (
              <HStack gap={2}>
                <Icon as={Clock} color="orange.600" boxSize={3} />
                <Text fontSize="xs" color="orange.600">
                  Resets in <strong>{resetTime}</strong>
                </Text>
              </HStack>
            )}
            
            {/* Total usage (optional) */}
            {freeTrialInfo && freeTrialInfo.total_free_analyses > 0 && (
              <Text fontSize="xs" color={canUseTrial ? "purple.500" : "orange.500"}>
                📊 Total free scans used: {freeTrialInfo.total_free_analyses}
              </Text>
            )}
          </VStack>
        </HStack>

        {/* Right side: Subscribe button */}
        <Button
          onClick={handleSubscribe}
          isLoading={creatingPayment}
          colorScheme={canUseTrial ? "purple" : "orange"}
          size="sm"
          flexShrink={0}
        >
          <HStack gap={2}>
            <Icon as={CreditCard} boxSize={4} />
            <span>Subscribe Now</span>
          </HStack>
        </Button>
      </HStack>
    </Box>
  );
}

